from dotenv import load_dotenv
import os
import uvicorn

load_dotenv()

PORT = int(os.getenv('PORT', 8000))

if __name__ == '__main__':
    uvicorn.run('app:app', port=PORT, reload=True)
