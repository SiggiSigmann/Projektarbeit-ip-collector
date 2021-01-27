ALTER TABLE Measurement 
ADD Country varchar(255), 
ADD Region varchar(255), 
ADD City varchar(255);

update Measurement set Country = "-", Region = "-", City  = "-";