from utils.connection import get_snowpark_session
from snowflake.snowpark import DataFrame
import snowflake.snowpark.types as T
import snowflake.snowpark.functions as F
from snowflake.snowpark import Window as W
import logging
import sys

# initiate logging at info level
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%I:%M:%S')


def filter_dataset(df, column_name, filter_criterian) -> DataFrame :
    return_df = df.filter(F.col(column_name) == filter_criterian)
    return return_df

def main():
    session = get_snowpark_session()
    #get the session object and get dataframe
    session = get_snowpark_session()
    sales_df = session.sql("select * from us_sales_order")

    # apply filter to select only paid and delivered sale orders
    # select * from us_sales_order where PAYMENT_STATUS = 'Paid' and SHIPPING_STATUS = 'Delivered'
    paid_sales_df = filter_dataset(sales_df,'PAYMENT_STATUS','Paid')
    shipped_sales_df = filter_dataset(paid_sales_df,'SHIPPING_STATUS','Delivered')

    # adding country and region to the data frame
    # select *, 'IN' as Country, 'APAC' as Region from us_sales_order where PAYMENT_STATUS = 'Paid' and SHIPPING_STATUS = 'Delivered'
    country_sales_df = shipped_sales_df.with_column('Country',F.lit('US')).with_column('Region',F.lit('NA'))

    # join to add forex calculation
    forex_df = session.sql("select * from sales_dwh.common.exchange_rate")
    sales_with_forext_df = country_sales_df.join(forex_df,country_sales_df['order_dt']==forex_df['echange_rate_dt'],join_type='outer')
    #sales_with_forext_df.show(2)

    #de-duplication
    print(sales_with_forext_df.count())
    unique_orders = sales_with_forext_df.with_column('order_rank',F.rank().over(W.partitionBy(F.col("order_dt")).order_by(F.col('_metadata_last_modified').desc()))) \
                                                                                .filter(F.col("order_rank")==1) \
                                                                                .select(F.col('SALES_ORDER_KEY').alias('unique_sales_order_key'))
    
    final_sales_df = unique_orders.join(sales_with_forext_df,unique_orders['unique_sales_order_key']==sales_with_forext_df['SALES_ORDER_KEY'],join_type='inner')
    
    final_sales_df = final_sales_df.select(
        F.col('SALES_ORDER_KEY'),
        F.col('ORDER_ID'),
        F.col('ORDER_DT'),
        F.col('CUSTOMER_NAME'),
        F.col('MOBILE_KEY'),
        F.col('Country'),
        F.col('Region'),
        F.col('ORDER_QUANTITY'),
        F.lit('USD').alias('LOCAL_CURRENCY'),
        F.col('UNIT_PRICE').alias('LOCAL_UNIT_PRICE'),
        F.col('PROMOTION_CODE').alias('PROMOTION_CODE'),
        F.col('FINAL_ORDER_AMOUNT').alias('LOCAL_TOTAL_ORDER_AMT'),
        F.col('TAX_AMOUNT').alias('local_tax_amt'),
        F.col('USD2INR').alias("Exhchange_Rate"),
        (F.col('FINAL_ORDER_AMOUNT')/F.col('USD2USD')).alias('US_TOTAL_ORDER_AMT'),
        (F.col('TAX_AMOUNT')/F.col('USD2USD')).alias('USD_TAX_AMT'),
        F.col('payment_status'),
        F.col('shipping_status'),
        F.col('payment_method'),
        F.col('payment_provider'),
        F.col('phone').alias('conctact_no'),
        F.col('shipping_address')
    )

    #final_sales_df.show(5)
    final_sales_df.write.save_as_table("sales_dwh.curated.us_sales_order",mode="append")


if __name__ == '__main__':
    main()