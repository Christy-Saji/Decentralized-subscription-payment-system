# 🔗 Decentralized Subscription Payment System

A Web3-powered subscription platform built on Ethereum that eliminates payment intermediaries, enabling transparent, censorship-resistant, and globally accessible subscriptions.

## 🌐 Live Demo

**🚀 [Try it Live](https://decentralized-subscription-payment.vercel.app/)**

**📊 [View Smart Contract on Etherscan](https://sepolia.etherscan.io/address/0x9149892d0162309Fe6b751a5f804e1816f934D43)**

---

## 🎯 Problem Statement

Traditional subscription systems have critical flaws:
- 💳 **Payment Data Risk**: Companies store sensitive credit card information
- 🌍 **Geographic Restrictions**: Services unavailable in many countries
- 🚫 **Arbitrary Censorship**: Platforms can ban users without recourse
- 💰 **Hidden Fees**: Processing fees (2.9% + $0.30) and price changes
- 🔒 **No Transparency**: Subscriber counts and revenue can be manipulated
- 🎭 **Privacy Concerns**: Personal data sold to advertisers

---

## ✨ Our Solution

A blockchain-based subscription system where:
- ✅ Users control their money via MetaMask wallet
- ✅ Fixed pricing enforced by immutable smart contract
- ✅ Complete transparency - all data verifiable on-chain
- ✅ Global accessibility - works anywhere with internet
- ✅ Censorship-resistant - no central authority
- ✅ Privacy-preserving - only wallet addresses stored

---

## 🏗️ Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                         User                                │
│                    (MetaMask Wallet)                        │
└────────────┬────────────────────────────────────────────────┘
             │
             │ 1. Connect Wallet
             │ 2. Subscribe (0.001 ETH)
             │ 3. View Status
             │
┌────────────▼────────────────────────────────────────────────┐
│                    Frontend (Vercel)                        │
│              HTML + JavaScript + ethers.js                  │
│         https://decentralized-subscription-payment          │
│                    .vercel.app                              │
└────────────┬────────────────────────────────────────────────┘
             │
             │ Web3 RPC Calls
             │
┌────────────▼────────────────────────────────────────────────┐
│              Ethereum Sepolia Testnet                       │
│                                                             │
│  ┌───────────────────────────────────────────────────┐      │
│  │        Smart Contract (Solidity)                  │      │
│  │  - subscribe() - Pay 0.001 ETH for 30 days        │      │
│  │  - cancel() - Cancel subscription                 │      │
│  │  - isActive() - Check subscription status         │      │
│  │  - getExpiry() - Get expiration timestamp         │      │
│  │                                                   │      │
│  │  Contract: 0x9149892d0162309Fe6b751a5f804e1816f934D43│   │
│  └───────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
```
---

## 🚀 Features

### Smart Contract (Solidity)
- **Fixed Pricing**: 0.001 ETH for 30-day subscription
- **Automatic Expiry**: Time-based subscription tracking
- **Instant Cancel**: Users can cancel anytime (no refunds)
- **Event Logging**: All actions emit blockchain events
- **Read Functions**: Anyone can verify subscription status
- **Immutable Logic**: Contract rules cannot be changed

### Frontend (HTML/JavaScript)
- **MetaMask Integration**: Secure wallet connection
- **Real-time Status**: Live subscription status updates
- **Transaction Handling**: Subscribe, renew, and cancel
- **Network Detection**: Automatic Sepolia network validation
- **Responsive Design**: Works on desktop and mobile
- **Live Stats**: Display total subscribers and revenue

### Backend API (Python/Flask)
- **Read-only Access**: No private keys stored
- **RESTful Endpoints**: JSON API for subscription data
- **Web3.py Integration**: Blockchain interaction layer
- **Error Handling**: Comprehensive error responses
- **CORS Enabled**: Accessible from any frontend

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Blockchain** | Ethereum (Sepolia Testnet) |
| **Smart Contract** | Solidity ^0.8.20 |
| **Frontend** | HTML, JavaScript, CSS |
| **Web3 Library** | ethers.js v5.7.2 |
| **Backend** | Python 3.12, Flask 3.0 |
| **Blockchain SDK** | web3.py 6.20 |
| **Deployment** | Vercel (Frontend) |
| **Version Control** | Git, GitHub |
| **Wallet** | MetaMask |
| **RPC Provider** | Infura / Public Sepolia RPCs |

---

## 📋 Prerequisites

- **MetaMask Wallet**: [Install MetaMask](https://metamask.io)
- **Sepolia ETH**: Get free test ETH from [Google Cloud Faucet](https://cloud.google.com/application/web3/faucet/ethereum/sepolia)
- **Python 3.8+**: For running backend locally
- **Git**: For version control

---

## 📖 Usage Guide For Users

1. **Visit the App**: Go to [https://decentralized-subscription-payment.vercel.app/](https://decentralized-subscription-payment.vercel.app/)

2. **Connect Wallet**:
   - Click "Connect MetaMask"
   - Approve connection in MetaMask popup
   - Ensure you're on Sepolia network

3. **Get Test ETH** (if needed):
   - Visit [Google Cloud Faucet](https://cloud.google.com/application/web3/faucet/ethereum/sepolia)
   - Enter your wallet address
   - Receive 0.05 Sepolia ETH

4. **Subscribe**:
   - Click "Subscribe Now - 0.001 ETH"
   - Confirm transaction in MetaMask
   - Wait 10-30 seconds for confirmation

5. **Check Status**:
   - View your subscription expiry date
   - See remaining time
   - Monitor subscription state

6. **Manage Subscription**:
   - **Renew**: Pay 0.001 ETH to extend 30 more days
   - **Cancel**: Cancel immediately (no refund)


#### Smart Contract Interaction (Remix)
1. Go to [Remix IDE](https://remix.ethereum.org)
2. Load contract at `0x9149892d0162309Fe6b751a5f804e1816f934D43`
3. Connect MetaMask to Sepolia
4. Call functions directly

---

## 🔐 Smart Contract Details

**Network**: Ethereum Sepolia Testnet  
**Contract Address**: `0x9149892d0162309Fe6b751a5f804e1816f934D43`  
**Compiler Version**: Solidity ^0.8.20  
---

### Constants
- **Subscription Price**: 0.001 ETH
- **Duration**: 30 days (2,592,000 seconds)
---

## 🎨 Workflow

### User Subscription Flow
```
1. User visits dApp
   ↓
2. Clicks "Connect MetaMask"
   ↓
3. MetaMask popup appears → User approves
   ↓
4. dApp displays subscription status (inactive)
   ↓
5. User clicks "Subscribe Now - 0.001 ETH"
   ↓
6. MetaMask popup → User confirms transaction
   ↓
7. Transaction sent to Ethereum network
   ↓
8. Smart contract executes subscribe() function
   ↓
9. Contract records: subscriptionExpiry[user] = now + 30 days
   ↓
10. Transaction confirmed (10-30 seconds)
   ↓
11. dApp updates UI → Shows "Active" status
   ↓
12. User has 30 days of access
```


## 📊 Current Stats (Live Data)

Visit [https://decentralized-subscription-payment.vercel.app/](https://decentralized-subscription-payment.vercel.app/) to see:
- Total active subscribers
- Total revenue collected (ETH)
- Real-time subscription status
- Live blockchain data


---

## 🤝 Use Cases

1. **Content Creators**: Direct fan subscriptions without platform fees
2. **SaaS Products**: Decentralized subscription management
3. **Online Courses**: Censorship-resistant educational access
4. **Premium APIs**: Token-gated API access control
5. **Membership Communities**: DAO-based membership systems
6. **Newsletter Platforms**: Direct writer-to-reader payments
7. **Streaming Services**: Decentralized content subscriptions

---

