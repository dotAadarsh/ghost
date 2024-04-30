# GHOST
Where Privacy Meets Intelligence!

![ghost-readme](https://github.com/dotAadarsh/ghost/assets/71810927/a96eb377-0fd8-4dd7-bad0-4176964c75ee)


[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/dotaadarsh/ghost)


## The Problem

When people use AI platforms, they might unknowingly leak sensitive information, which can be a real problem. It could happen when they share personal details without realizing it or accidentally reveal confidential stuff during interactions. This kind of slip-up can have serious consequences for privacy and security. So, it's crucial for users to be careful about what they share and understand how AI systems work. Plus, companies need to have strong safeguards in place to protect data and make sure users know how to use these systems safely.

## Solution

One effective solution to mitigate the risk of sensitive information leakage in AI usage is by implementing redaction and file sanitization measures. Redacting sensitive information involves selectively removing or obscuring confidential details from documents or inputs before they are processed by AI systems. Similarly, sanitizing files ensures that any potentially compromising data is cleansed or anonymized prior to analysis or sharing. These practices help safeguard privacy and security by minimizing the exposure of sensitive information while still allowing users to benefit from AI technologies. Additionally, incorporating encryption and access controls further enhances data protection measures, ensuring that only authorized individuals can access or manipulate sensitive data within AI environments.

## What GHOST do?

GHOST is an AI chatbot powered by Pangea. You may wonder why another bot? The aim is to showcase how a chatbot can be enhanced to be safer and more trustworthy. With Pangea's Redaction and file sanitization feature, we can utilize AI without concerns about the leakage of sensitive/personal information.

I have utilized Google's Gemini 1.5 Pro AI model to respond to queries. The uploaded PDF is sanitized before processing using [Pangea's Sanitize feature](https://pangea.cloud/docs/sanitize/). For vectorizing the content from the PDF, I employed [Cohere's Embeddings](https://docs.cohere.com/docs/embeddings). These embeddings identify similar contexts based on user input, which are then passed to the Gemini AI for question-answering.

## How I built it

### Redaction

Every prompt will go through the Redaction process before it reaches the AI. For this I have used [Pangea's Redact Service](https://pangea.cloud/docs/redact/). It comes with predefined rules designed to handle various forms of sensitive data such as personally identifiable information (PII), geographic locations, payment card industry (PCI) data, and more. 

Any uploaded PDF file, before processing, will be sanitized which analyze and cleans potentially harmful files, removing any actionable or potentially harmful content and links and redacting the sensitive info in the uploaded file. This is done with the help of [Pangea's Sanitize feature](https://pangea.cloud/docs/sanitize/). 

Due to the token limit, We can't directly send the contents from the PDF. So in order to resolve that I have used vector embeddings. The sanitized file is processed with[ LLM Sherpa](https://github.com/nlmatics/llmsherpa), which is a tool is designed to help developers work more efficiently with LLMs by providing a set of APIs that can handle various tasks, such as parsing documents, extracting layout information, and facilitating better indexing and retrieval processes. After extracting the content from PDF, it is then converted into vector embeddings by Cohere Embeddings API. Based on the input query, cohere gives us the relatable contexts which are then sent to the Gemini AI for question/answering. 

## How to run?

1. Clone the repo
2. Install the required modules from the requiremets.txt
3. Add your API Keys in the .streamlit/secrets.toml file
4. Run the app by `streamlit run Home.py`

## Challenges we ran into

Playing with the API was interesting and challenging to make it work with the UI. Writing multiple functions, and to be honest, naming the variable is quite a hard task for me, ran into different errors but hey, a different error message is always a step forward :) which keeps me motivated.

## What I learned

It was a great learning experience for me, starting from Python to the Secure by Design principle. Along the way, I delved into topics such as APIs, functions, vector embeddings, AI, and beyond.

## What's next for GHOST

I was thinking, why can't I create a Chrome extension that redacts all the sensitive info (if it's turned on) on all websites if the user tries to enter it? 

Another concept involves customer service routinely processing our audio for training purposes. A tool could be developed for companies to automatically redact sensitive information from these recordings, enabling them to proceed with further processing in compliance with privacy regulations and industry guidelines. This can be powered by [OpenAI's Whisper Model](https://github.com/openai/whisper) and Pangea's Services.

## References

- [Pangea | Documentation](https://pangea.cloud/docs/)
- [Streamlit Docs - API reference](https://docs.streamlit.io/develop/api-reference)
- [Cohere AI - Embeddings](https://docs.cohere.com/docs/embeddings)

Thanks for the read! Let me know if anything, always open to feedback. 

