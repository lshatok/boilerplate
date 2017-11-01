DELIMITER $$
CREATE PROCEDURE meterDataSplits(tenantId varchar(60),  nSplits int)
BEGIN
	DECLARE i,j,k INT DEFAULT 0;
	DECLARE str VARCHAR(60000);
	DECLARE aStr VARCHAR(60);	
	SELECT COUNT(*) INTO i FROM meters;
	SELECT FLOOR(COUNT(*)/nSplits) INTO j FROM meters;
	SET k = j;
	SET str = CONCAT('create \'meter_data_', tenantId, '\',{NAME => \'actual\', COMPRESSION => \'SNAPPY\'}, {SPLITS => [');
	simple_loop: LOOP
		set aStr = ''; 
		SELECT meter_identifier INTo aStr FROM meters ORDER BY meter_identifier LIMIT 1 OFFSET k;
		SET str = CONCAT(str, '\'',aStr,'\'');
		SET k=k+j;
		IF k >= i then 
			SET str = CONCAT(str, ']}');
			LEAVE simple_loop;
		 ELSE
			SET str = CONCAT(str, ',');
         END IF;
	END LOOP simple_loop; 

	SELECT str;
END $$

DELIMITER ;

call meterDataSplits('oge_prod', 70);

DROP PROCEDURE meterDataSplits;