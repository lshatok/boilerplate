Meter Data Splits:

My SQL store procedure will automatically create the HBase create statement with splits 
based on the no of meters and regions.

Call the store procedure with arguments tenant id and no of splits

Steps:
1. Login to the workbench
2. Compile the store procedure
3. CALL meterDataSplits(<Tenant id>, <Splits>)  Example : CALL meterDataSplits('oge_prod', 70);  
4. copy the output to Hbase shell
5. DROP PROCEDURE meterDataSplits;