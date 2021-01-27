CREATE DATABASE networkdata;

USE networkdata;

CREATE USER 'test'@'%' IDENTIFIED BY '1234567';
GRANT ALL PRIVILEGES ON networkdata . * TO 'test'@'%';

CREATE TABLE Tracert (
    TraceID int AUTO_INCREMENT,
    IpAddress varchar(255),
    AddressName varchar(255),
    Hop int,
    PRIMARY KEY (TraceID, Hop)
);

ALTER TABLE Tracert AUTO_INCREMENT=0;

CREATE TABLE Measurement (
    MeasurementID INT AUTO_INCREMENT,
    PersonName varchar(255),
    IpAddress varchar(255),
    TraceID int,
    IpTimestamp DATETIME NOT NULL,
    Country varchar(255), 
    Region varchar(255), 
    City varchar(255),
    FOREIGN KEY (TraceID) REFERENCES Tracert(TraceID),
    PRIMARY KEY (MeasurementID)
);

ALTER TABLE Measurement AUTO_INCREMENT=0;



