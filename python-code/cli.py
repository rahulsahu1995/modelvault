import argparse
import requests

def generate(prompt: str, url: str):
    try:
        response = requests.post(url, json={"prompt": prompt})
        response.raise_for_status()
        response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")

def generate_stream(prompt: str, url: str):
    try:
        with requests.post(url, json={"prompt": prompt}, stream=True) as response:
            response.raise_for_status()
            for chunk in response.iter_content(chunk_size=1024, decode_unicode=True):
                if chunk:
                    print(chunk, end="", flush=True)
            print("\n")
    except requests.RequestException as e:
        print(f"Streaming request failed: {e}")

def main():
    parser = argparse.ArgumentParser(description="Send prompt to MiniVault API")
    parser.add_argument("--prompt", required=True, help="Prompt text to send")
    parser.add_argument("--url", default="http://127.0.0.1:3000/generate", help="API endpoint URL")
    parser.add_argument("--stream", action="store_true", help="Use streaming endpoint")
    args = parser.parse_args()

    if args.stream:
        generate_stream(args.prompt, args.url.replace("/generate", "/generate-stream"))
    else:
        generate(args.prompt, args.url)

if __name__ == "__main__":
    main()
