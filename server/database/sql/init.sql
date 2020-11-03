CREATE DATABASE networkdata;

USE networkdata;

CREATE USER 'test'@'%' IDENTIFIED BY '1234567';
GRANT ALL PRIVILEGES ON networkdata . * TO 'test'@'%';

CREATE TABLE Tracert (
    TraceID int AUTO_INCREMENT PRIMARY KEY,
    IpAddress varchar(255),
    AddressName varchar(255),
    Hop int
);

CREATE TABLE Measurement (
    MeasurementID INT AUTO_INCREMENT PRIMARY KEY,
    PersonName varchar(255),
    IpAddress varchar(255),
    TraceID int,
    IpTimestamp DATETIME NOT NULL,
    FOREIGN KEY (TraceID) REFERENCES Tracert(TraceID)
);



