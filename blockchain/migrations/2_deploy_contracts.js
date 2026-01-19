const CertiChain = artifacts.require("CertiChain");

module.exports = function (deployer) {
  deployer.deploy(CertiChain);
};
