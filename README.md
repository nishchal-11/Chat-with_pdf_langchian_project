# 📄 Chat with Your PDF

A conversational AI application that allows you to upload PDF documents and have interactive chat conversations about their content using LangChain and Google's Generative AI.

## 🚀 Features

- **PDF Upload & Processing**: Upload any PDF document and automatically extract text content
- **Intelligent Chat**: Ask questions about your PDF and get context-aware answers
- **Conversational Memory**: Maintains chat history for natural, contextual conversations
- **Vector Search**: Uses Chroma vector database for efficient document retrieval
- **Modern UI**: Clean Streamlit interface for easy interaction
- **Secure**: API keys stored in environment variables

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI/ML**: LangChain, Google Generative AI (Gemini)
- **Vector Database**: Chroma
- **PDF Processing**: PyPDFLoader
- **Language**: Python 3.8+

## 📋 Prerequisites

- Python 3.8 or higher
- Google Cloud API key with Generative AI enabled
- Internet connection for API calls

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/nishchal-11/Chat-with_pdf_langchian_project.git
   cd Chat-with_pdf_langchian_project
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Create a `.env` file in the root directory
   - Add your Google API key:
     ```
     GOOGLE_API_KEY=your_google_api_key_here
     ```

## 🚀 Usage

1. **Run the application**
   ```bash
   streamlit run project_pdf_chat.py
   ```

2. **Open your browser**
   - Navigate to `http://localhost:8502`

3. **Start chatting**
   - Upload a PDF document using the sidebar
   - Wait for processing to complete
   - Ask questions about the document content
   - Continue the conversation naturally

## 📁 Project Structure

```
Chat-with_pdf_langchian_project/
├── project_pdf_chat.py      # Main application file
├── .env                     # Environment variables (not committed)
├── .gitignore              # Git ignore rules
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## 🔑 API Setup

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your `.env` file as `GOOGLE_API_KEY`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LangChain](https://www.langchain.com/) for the RAG framework
- [Google Generative AI](https://ai.google.dev/) for the language model
- [Streamlit](https://streamlit.io/) for the web interface
- [Chroma](https://www.trychroma.com/) for vector storage

## 📞 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check the troubleshooting section below

## 🔧 Troubleshooting

**Common Issues:**

1. **"No current event loop" error**
   - This is fixed in the current version using REST transport
   - Make sure you're using the latest code

2. **API Key errors**
   - Verify your `.env` file exists and contains the correct API key
   - Check that your Google Cloud project has Generative AI API enabled

3. **PDF processing fails**
   - Ensure the PDF is not password-protected
   - Check that the PDF contains extractable text (not just images)

4. **Port already in use**
   - Change the port: `streamlit run project_pdf_chat.py --server.port 8503`

## 📈 Future Enhancements

- [ ] Support for multiple PDF uploads
- [ ] Export chat history
- [ ] Dark mode theme
- [ ] Integration with other document formats
- [ ] User authentication
- [ ] Cloud deployment options

---

**Made with ❤️ using LangChain and Google AI**
