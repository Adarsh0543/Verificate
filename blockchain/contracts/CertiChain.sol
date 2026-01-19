// SPDX-License-Identifier: MIT
pragma solidity ^0.5.16;
pragma experimental ABIEncoderV2;

contract CertiChain {
    /////////////////////////////
    // Institution Section
    /////////////////////////////
    struct Institution {
        string institutionName;
        string affiliation;
        string regNumber;
        string dateOfEstablishment;
        string institutionType; 
        string streetAddress;
        string city;
        string state;
        string postalCode;
        string country;
        string officialEmail;
        string phoneNumber;
        string adminName;
        string adminDesignation;
        string adminEmail;
        string adminPhone;
        bool exists;
    }
    
    mapping(string => Institution) private institutions;
    // Additional mappings for uniqueness checks:
    mapping(string => bool) private registeredRegNumbers;
    mapping(string => bool) private registeredOfficialEmails;
    mapping(string => bool) private registeredInstitutionNames;
    
    event InstitutionRegistered(string institutionID);

    function registerInstitution(
        string memory _institutionID,
        Institution memory _institution
    ) public {
        require(!institutions[_institutionID].exists, "Institution ID already registered");
        require(!registeredRegNumbers[_institution.regNumber], "Institution with this Registration Number already exists");
        require(!registeredOfficialEmails[_institution.officialEmail], "Institution with this Official Email already exists");
        require(!registeredInstitutionNames[_institution.institutionName], "Institution with this Name already exists");
        
        // Store the institution details
        institutions[_institutionID] = _institution;
        
        // Mark the unique fields as registered
        registeredRegNumbers[_institution.regNumber] = true;
        registeredOfficialEmails[_institution.officialEmail] = true;
        registeredInstitutionNames[_institution.institutionName] = true;
        
        emit InstitutionRegistered(_institutionID);
    }
    
    function getInstitution(string memory _institutionID) public view returns (Institution memory) {
        require(institutions[_institutionID].exists, "Institution not registered");
        return institutions[_institutionID];
    }
    
    /////////////////////////////
    // Certificate Section
    /////////////////////////////
    struct Certificate {
        string certID;
        string studentName;
        string course;
        string issueDate;
        string dob;                   // Date of birth of the certificate recipient
        string courseDuration;
        string issuingAuthorityName;  // Name of the certificate issuing authority
        string userEmail;             // User's email address (linking certificate to the user)
        bool exists;
    }
    
    mapping(string => Certificate) private certificates;
    
    event CertificateIssued(string certID, string issuingAuthorityName);
    
    function issueCertificate(
        string memory _certID,
        string memory _studentName,
        string memory _course,
        string memory _issueDate,
        string memory _dob,
        string memory _courseDuration,
        string memory _issuingAuthorityName,
        string memory _userEmail
    ) public {
        require(!certificates[_certID].exists, "Certificate already issued");
        certificates[_certID] = Certificate(
            _certID, 
            _studentName, 
            _course, 
            _issueDate, 
            _dob, 
            _courseDuration, 
            _issuingAuthorityName,
            _userEmail,
            true
        );
        emit CertificateIssued(_certID, _issuingAuthorityName);
    }
    
    function getCertificate(string memory _certID) public view returns (Certificate memory) {
        require(certificates[_certID].exists, "Certificate not found");
        return certificates[_certID];
    }
    
    // New: Event to signal that a certificate has been revoked
    event CertificateRevoked(string certID);
    
    // New: Function to revoke a certificate
    function revokeCertificate(string memory _certID) public {
        require(certificates[_certID].exists, "Certificate not found or already revoked");
        certificates[_certID].exists = false;
        emit CertificateRevoked(_certID);
    }
    
    /////////////////////////////
    // User Section
    /////////////////////////////
    struct UserProfile {
        string userId;      // Unique user ID
        string name;
        string dob;
        string phoneNumber;
        string country;
        string pincode;
        string streetAddress;
        string city;
        string state;
        string email;       // User's login email
        bool exists;
    }
    
    mapping(string => UserProfile) private userProfiles;
    
    event UserRegistered(string userId);
    
    function registerUser(string memory _userId, UserProfile memory _profile) public {
        require(!userProfiles[_userId].exists, "User already registered");
        userProfiles[_userId] = _profile;
        userProfiles[_userId].exists = true;
        emit UserRegistered(_userId);
    }
    
    function getUser(string memory _userId) public view returns (UserProfile memory) {
        require(userProfiles[_userId].exists, "User not registered");
        return userProfiles[_userId];
    }
    
    // Helper function to check if a user is registered
    function isUserRegistered(string memory _userId) public view returns (bool) {
        return userProfiles[_userId].exists;
    }
}
