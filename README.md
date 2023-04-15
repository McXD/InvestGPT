# InvestGPT

<!-- TOC -->
* [InvestGPT](#investgpt)
  * [Quick Start](#quick-start)
  * [Implementation Details](#implementation-details)
    * [Session-based Storage](#session-based-storage)
    * [Deciding When to Call API](#deciding-when-to-call-api)
  * [Credit](#credit)
<!-- TOC -->

A COMP4531 Project. Use GPT-3.5 to map user risk profile and use our own API and database to suggest investment portfolio.

## Quick Start

Make sure you have OpenAI API key stored in .env file (`OPENAI_API_KEY`)

```bash
# Proxy
pip install -r requirements.txt
python app.py # :5000

# Client
cd client
npm install
npm start # :3000
```

## Implementation Details

### Session-based Storage

The simple demo app does not have an account system. Instead, we use session-based (flask-session) storage to store user's conversation history in a single session. **When you refresh the frontend, you will start a new conversation.**

### Deciding When to Call API

We've instructed GPT to signal to us when the user data is sufficient to make an API call by let it including a structured data (i.e., JSON) in the response. We then parse the response and make the corresponding API call.

## Credit

React client is adapted from [react-openai-chat](https://github.com/trananhtuat/react-openai-chat).
