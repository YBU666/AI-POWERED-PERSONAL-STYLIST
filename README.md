# AI-Powered Personal Stylist and Virtual Try-On Assistant

## Project Overview
The AI-Powered Personal Stylist and Virtual Try-On Assistant is a Django-based web application that revolutionizes personal styling through advanced AI integration. This project addresses the gap in accessible fashion advice by combining cutting-edge AI technologies to deliver personalized outfit recommendations and virtual try-on experiences, specifically tailored for Indian users.

## Key Features
- Personalized outfit recommendations based on user profiles
- AI-generated outfit visualizations
- Photorealistic virtual try-on capabilities
- User profile management with detailed preferences
- Style preference learning
- Shopping recommendations

## Technical Stack

### AI Integration
- **Groq's LLM (llama-3.3-70b-versatile)**
  - Personalized outfit recommendations
  - Intelligent style analysis
  - Context-aware suggestions

- **Hugging Face's Stable Diffusion XL (SDXL)**
  - txt2img for outfit generation
  - img2img for photorealistic virtual try-ons
  - Optimized for Indian demographics

### Backend Technologies
- **Python 3.11+**
  - Primary backend language
- **Django 4.x**
  - Web framework
- **SQLite3**
  - Database backend
- **python-dotenv**
  - Secure API key management

### Frontend Technologies
- **Bootstrap 5**
  - Responsive design framework
- **Animate.css**
  - Smooth animations
- **Font Awesome**
  - Icon library
- **Glass morphism CSS**
  - Modern UI elements

## User Profile Features
The application captures comprehensive user information including:
- Gender
- Body type
- Height
- Skin tone
- Event contexts
- Climate preferences
- Style preferences

## AI Implementation Details
- **Styling Engine**
  - Temperature: 0.7
  - Structured JSON outputs
  - Detailed outfit descriptions
  - Shopping keywords generation

- **Virtual Try-on Module**
  - High-quality image generation
  - Accurate texture representation

## Architecture
The application follows Django's MVT (Model-View-Template) architecture with:
- Robust error handling
- Loading states
- User guidance systems
- Secure API key management
- Responsive design implementation

## Getting Started
1. Clone the repository
2. Install dependencies
3. Set up environment variables for API keys:
   - Groq API Key (LLaMA-3.3)
   - Hugging Face API (SDXL)
   - Rapid API Key (Try-on Diffusion)
4. Run migrations
5. Start the development server

## Future Enhancements
- Advanced style preference learning
- Style diary/lookbook feature
- Enhanced virtual try-on capabilities

##Screenshots
![images](https://github.com/YBU666/AI-POWERED-PERSONAL-STYLIST.git/blob/main/a1.png?raw=true)
![images](https://github.com/YBU666/AI-POWERED-PERSONAL-STYLIST.git/blob/main/a2.png?raw=true)
![images](https://github.com/YBU666/AI-POWERED-PERSONAL-STYLIST.git/blob/main/a3.png?raw=true)
![images](https://github.com/YBU666/AI-POWERED-PERSONAL-STYLIST.git/blob/main/a4.png?raw=true)
![images](https://github.com/YBU666/AI-POWERED-PERSONAL-STYLIST.git/blob/main/a5.png?raw=true)
![images](https://github.com/YBU666/AI-POWERED-PERSONAL-STYLIST.git/blob/main/a6.png?raw=true)
![images](https://github.com/YBU666/AI-POWERED-PERSONAL-STYLIST.git/blob/main/a7.png?raw=true)
![images](https://github.com/YBU666/AI-POWERED-PERSONAL-STYLIST.git/blob/main/a8.png?raw=true)
![images](https://github.com/YBU666/AI-POWERED-PERSONAL-STYLIST.git/blob/main/a9.png?raw=true)
![images](https://github.com/YBU666/AI-POWERED-PERSONAL-STYLIST.git/blob/main/a10.png?raw=true)
![images](https://github.com/YBU666/AI-POWERED-PERSONAL-STYLIST.git/blob/main/a11.png?raw=true)
![images](https://github.com/YBU666/AI-POWERED-PERSONAL-STYLIST.git/blob/main/a12.png?raw=true)
![images](https://github.com/YBU666/AI-POWERED-PERSONAL-STYLIST.git/blob/main/a13.png?raw=true)
![images](https://github.com/YBU666/AI-POWERED-PERSONAL-STYLIST.git/blob/main/a14.png?raw=true)



## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Project Structure
```
ai_stylist_project/
├── ai_stylist/            # Django project settings
├── stylist/               # Main application
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── forms.py           # Form definitions
│   └── urls.py            # URL routing
├── templates/             # HTML templates
│   └── stylist/
│       ├── base.html      # Base template
│       ├── home.html      # Homepage
│       ├── profile.html   # User profile
│       └── ...            # Other templates
├── static/                # Static files (CSS, JS)
└── media/                 # User uploaded files
```


