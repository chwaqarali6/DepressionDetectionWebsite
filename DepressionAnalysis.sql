CREATE DATABASE DepressionAnalysis

CREATE TABLE Patient(
	PatientID INT AUTO_INCREMENT PRIMARY KEY,
	PatientName VARCHAR(50) NOT NULL,
    CNIC VARCHAR(50),
	Email VARCHAR(50),
	Contact VARCHAR(50),
    Address VARCHAR(150),
    CheckInDate VARCHAR(50),
	Comments VARCHAR(150),
    DepressionStatus VARCHAR(50),
    AssignedDoctorID INT
)

CREATE TABLE Doctor(
	DoctorID INT AUTO_INCREMENT PRIMARY KEY,
	DoctorName VARCHAR(50) NOT NULL,
	DoctorEmail VARCHAR(50) NOT NULL,
	DoctorPassword VARCHAR(50) NOT NULL
)

ALTER TABLE Patient ADD FOREIGN KEY (AssignedDoctorID) REFERENCES Doctor(DoctorID)


DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `SignIn` (P_DoctorEmail VARCHAR(50),P_DoctorPassword VARCHAR(50))
BEGIN
    SELECT * FROM Doctor WHERE P_DoctorEmail=DoctorEmail AND P_DoctorPassword=DoctorPassword;
END$$
DELIMITER ;



DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `AddPatient`(P_PatientName VARCHAR(50),P_CNIC VARCHAR(50),
P_Email VARCHAR(50),P_Contact VARCHAR(50),P_Address VARCHAR(150),P_CheckInDate VARCHAR(50),
P_Comments VARCHAR(150))
BEGIN
    IF ( SELECT EXISTS (SELECT 1 FROM Patient WHERE PatientName = P_PatientName)) THEN
        SELECT 'Patient Exists!';
    ELSE
        INSERT INTO Patient(PatientName,CNIC,Email,Contact,Address,CheckInDate,Comments)
        VALUES(P_PatientName,P_CNIC,P_Email,P_Contact,P_Address,P_CheckInDate,P_Comments);
    END IF;
END$$
DELIMITER ;


DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `DepressionStatus` (P_PatientID INT, P_PatientStatus VARCHAR(50))
BEGIN
	UPDATE Patient SET	DepressionStatus = P_PatientStatus WHERE  P_PatientID = PatientID;
END$$
DELIMITER ;


DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `ViewAllPatients` ()
BEGIN
    SELECT * FROM Patient ;
END$$
DELIMITER ;


DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `SearchByName` (P_SearchingName VARCHAR(50))
BEGIN
    SELECT * FROM Patient WHERE PatientName LIKE CONCAT('%', P_SearchingName , '%');
END$$
DELIMITER ;


DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `SearchByDate` (P_SearchingDate VARCHAR(50))
BEGIN
    SELECT * FROM Patient WHERE P_SearchingDate = CheckInDate ;
END$$
DELIMITER ;


DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `DeletePatient` (P_PatientID INT)
BEGIN
    DELETE FROM Patient WHERE P_PatientID = PatientID ;
END$$
DELIMITER ;


DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `PatientData` ()
BEGIN
    SELECT counts FROM((SELECT DepressionStatus, count(*) counts FROM Patient GROUP BY DepressionStatus)UNION(SELECT DepressionStatus, count(*) counts FROM Patient))T;
END$$
DELIMITER ;

UPDATE Patient SET DepressionStatus=NULL WHERE PatientID=1
ALTER TABLE Patient AUTO_INCREMENT = 1;
