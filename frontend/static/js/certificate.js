let contract;
let web3;

// Initialize Web3 and Contract
async function init() {
    if (window.ethereum) {
        web3 = new Web3(window.ethereum);
        try {
            await window.ethereum.request({ method: "eth_requestAccounts" });

            const contractABI = [
                {
                    "constant": true,
                    "inputs": [{ "internalType": "string", "name": "_certID", "type": "string" }],
                    "name": "getCertificate",
                    "outputs": [
                        { "internalType": "string", "name": "", "type": "string" },
                        { "internalType": "string", "name": "", "type": "string" },
                        { "internalType": "string", "name": "", "type": "string" }
                    ],
                    "payable": false,
                    "stateMutability": "view",
                    "type": "function"
                }
            ];

            const contractAddress = "0x9b1f7F645351AF3631a656421eD2e40f2802E6c0"; // Update if needed
            contract = new web3.eth.Contract(contractABI, contractAddress);
            console.log("✅ Contract Initialized:", contract);
        } catch (error) {
            console.error("⚠️ MetaMask Error:", error);
            alert("⚠️ Please unlock MetaMask to proceed.");
        }
    } else {
        alert("⚠️ Please install MetaMask to use this app.");
    }
}

// Get Certificate ID from URL
function getCertIDFromURL() {
    const pathParts = window.location.pathname.split("/"); // Split URL path
    const certID = pathParts[pathParts.length - 1]; // Get last part (certificate ID)
    
    console.log("Extracted certID:", certID); // Debugging log
    
    if (!certID || certID.trim() === "") {
        console.error("❌ No valid certID found in URL:", window.location.href);
        return null;
    }

    return certID;
}



// Fetch and display certificate details
async function fetchCertificateDetails() {
    const certId = getCertIDFromURL();
    if (!certId) {
        alert("❌ Invalid Certificate ID.");
        return;
    }

    if (!contract) {
        console.error("❌ Contract not initialized.");
        alert("⚠️ Blockchain connection error. Try again.");
        return;
    }

    try {
        console.log("Fetching details for certID:", certId);
        const certificate = await contract.methods.getCertificate(certId).call();
        console.log("Certificate data:", certificate); // Log fetched data

        if (certificate[0] !== "") {
            document.getElementById("certId")?.innerHTML = certId;
            document.getElementById("holderName")?.innerHTML = certificate[0];
            document.getElementById("issuer")?.innerHTML = certificate[1];
            document.getElementById("issueDate")?.innerHTML = certificate[2];
        } else {
            alert("❌ Certificate not found.");
            window.location.href = "/verify";
        }
    } catch (error) {
        console.error("❌ Error fetching certificate:", error);
        alert("⚠️ Error fetching certificate details.");
    }
}


// Ensure DOM is fully loaded before running the script
document.addEventListener("DOMContentLoaded", async () => {
    await init();
    fetchCertificateDetails();
});
