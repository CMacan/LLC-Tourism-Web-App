print("Before importing generativeai")
import google.generativeai as genai
print("After importing generativeai")
try:
    import google.generativeai as genai
    print("Import successful")
except ImportError as e:
    print(f"Import failed: {e}")
