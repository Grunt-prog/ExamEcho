import openai
import os

class OpenAIClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

    def generate_response(self, prompt: str, conversation_history: list = None) -> str:
        """
        Send a prompt to OpenAI with conversation history and get a response.

        Args:
            prompt: Current question from user
            conversation_history: List of {role, content} dicts from previous messages

        Returns:
            Response from OpenAI API
        """
        try:
            messages = [
                {
                    "role": "system",
                    "content": """You are an AWS Solutions Architect Associate exam tutor. 
                    
Your job is to give clear, concise, and exam-focused answers.

Rules:
- Keep every answer to 3-4 sentences maximum
- Get straight to the point — no filler, no lengthy intros
- Always explain acronyms the first time you use them, e.g. "Simple Storage Service (S3)" or "Identity and Access Management (IAM)"
- Focus only on what matters for the AWS SAA-C03 exam
- If comparing two things, clearly state the key difference in one sentence
- If there's an important exam tip or common mistake, include it in the final sentence
- For general concepts like networking, answer them directly and relate to AWS in one sentence
- Never use bullet points or lists — write in clean, flowing sentences
- Remember context from earlier in the conversation if relevant"""
                }
            ]

            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history)

            # Add current question
            messages.append({
                "role": "user",
                "content": prompt
            })

            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=0.5,
                max_tokens=300
            )

            return response.choices[0].message.content.strip()

        except openai.error.AuthenticationError:
            return "Error: Invalid OpenAI API key"
        except openai.error.RateLimitError:
            return "Error: Rate limit exceeded. Try again later"
        except openai.error.APIError as e:
            return f"Error: OpenAI API error - {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"

    def check_health(self) -> bool:
        """
        Check if OpenAI connection is valid
        """
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": "ping"}],
                max_tokens=5,
                timeout=5
            )
            return True
        except:
            return False