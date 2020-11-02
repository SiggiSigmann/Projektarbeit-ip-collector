CREATE DATABASE networkdata;

USE networkdata;

CREATE TABLE Tracert (
    TracertID int AUTO_INCREMENT PRIMARY KEY,
    DestIP varchar(255)
);

CREATE TABLE Measurement (
    MeasurementID INT AUTO_INCREMENT PRIMARY KEY,
    PersonName varchar(255),
    IpAddress varchar(255),
    IpTrace int,
    FOREIGN KEY (IpTrace) REFERENCES Tracert(TracertID),
    Timestamp DATETIME NOT NULL
);

CREATE TABLE Tracesetp (
    TraceID int AUTO_INCREMENT PRIMARY KEY,
    IpAddress varchar(255),
    AddressName varchar(255),
    TracertID int,
    FOREIGN KEY (TracertID) REFERENCES Tracert(TracertID)
);