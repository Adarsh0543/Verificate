let contract;
let accounts;
let web3;

// Initialize Web3 and Contract
async function init() {
    if (window.ethereum) {
        web3 = new Web3(window.ethereum);
        try {
            await window.ethereum.request({ method: "eth_requestAccounts" });
            accounts = await web3.eth.getAccounts();

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

            const contractAddress = "0x9b1f7F645351AF3631a656421eD2e40f2802E6c0";
            contract = new web3.eth.Contract(contractABI, contractAddress);
            console.log("✅ Contract Initialized:", contract);
        } catch (error) {
            console.error("⚠️ MetaMask Error:", error);
            if (error.code === 4001) {  
                alert("⚠️ MetaMask connection denied. Please allow access.");
            } else {
                alert("⚠️ MetaMask error: " + error.message);
            }
        }
    } else {
        alert("⚠️ Please install MetaMask to use this app.");
    }
}

// Event listener for Verify button
document.getElementById("verify-form").addEventListener("submit", async function(event) {
    event.preventDefault();

    await init(); // Ensure Web3 & contract are loaded

    let certId = document.getElementById("verifyCertId").value.trim();
    let certStatusElement = document.getElementById("certStatus");
    let viewDetailsButton = document.getElementById("viewDetailsBtn");

    if (!certId) {
        certStatusElement.innerText = "⚠️ Please enter a valid Certificate ID.";
        certStatusElement.style.color = "orange";
        viewDetailsButton.style.display = "none";
        return;
    }

    // Ensure contract is initialized
    if (!contract) {
        certStatusElement.innerText = "⚠️ Unable to connect to the blockchain.";
        certStatusElement.style.color = "red";
        return;
    }

    try {
        let certificate = await contract.methods.getCertificate(certId).call();

        if (certificate[0] !== "") {
            // Display verification success message
            certStatusElement.innerText = "✅ Successfully Verified!";
            certStatusElement.style.color = "green";

            // Show "View Details" button with correct URL format
            viewDetailsButton.style.display = "inline-block";
            viewDetailsButton.setAttribute("href", `/certificate/${certId}`);

        } else {
            certStatusElement.innerText = "❌ Certificate not found.";
            certStatusElement.style.color = "red";
            viewDetailsButton.style.display = "none";
        }
    } catch (error) {
        console.error("❌ Error verifying certificate:", error);
        certStatusElement.innerText = "⚠️ Error verifying certificate.";
        certStatusElement.style.color = "red";
        viewDetailsButton.style.display = "none";
    }
});

// Ensure Web3 initializes when the page loads
window.addEventListener("load", init);
