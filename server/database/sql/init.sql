CREATE DATABASE networkdata;

USE networkdata;

CREATE TABLE Measurement (
    MeasurementID INT AUTO_INCREMENT PRIMARY KEY,
    PersonName varchar(255),
    IpAddress varchar(255),
    IpTrace varchar(1000),
    Timestamp DATETIME NOT NULL
);