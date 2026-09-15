#!/usr/bin/env python3
"""A small command-line tool for checking URLs."""

import argparse
import csv
import json
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


def normalize_url(url: str) -> str:
    url = url.strip()
    if not url:
        return url
    if not url.startswith(("http://", "https://")):
        return "https://" + url
    return url


def check_url(url: str, timeout: float = 10.0) -> dict:
    url = normalize_url(url)
    parsed = urlparse(url)

    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return {
            "url": url,
            "status": "invalid",
            "status_code": "",
            "title": "",
            "response_time_ms": "",
            "error": "Invalid URL",
        }

    request = Request(
        url,
        headers={"User-Agent": "LinkInspector/1.0"},
        method="GET",
    )

    started = time.perf_counter()
    try:
        with urlopen(request, timeout=timeout) as response:
            body = response.read(256_000).decode("utf-8", errors="ignore")
            elapsed = round((time.perf_counter() - started) * 1000, 1)
            title = extract_title(body)
            return {
                "url": url,
                "status": "ok",
                "status_code": response.status,
                "title": title,
                "response_time_ms": elapsed,
                "error": "",
            }
    except HTTPError as exc:
        elapsed = round((time.perf_counter() - started) * 1000, 1)
        return {
            "url": url,
            "status": "http_error",
            "status_code": exc.code,
            "title": "",
            "response_time_ms": elapsed,
            "error": str(exc.reason),
        }
    except (URLError, TimeoutError, OSError) as exc:
        elapsed = round((time.perf_counter() - started) * 1000, 1)
        return {
            "url": url,
            "status": "error",
            "status_code": "",
            "title": "",
            "response_time_ms": elapsed,
            "error": str(exc.reason) if hasattr(exc, "reason") else str(exc),
        }


def extract_title(html: str) -> str:
    lower = html.lower()
    start = lower.find("<title")
    if start == -1:
        return ""
    start = lower.find(">", start)
    if start == -1:
        return ""
    end = lower.find("</title>", start)
    if end == -1:
        return ""
    return " ".join(html[start + 1:end].split())


def read_urls(path: str) -> list[str]:
    with open(path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip() and not line.lstrip().startswith("#")]


def print_results(results: list[dict]) -> None:
    for result in results:
        code = result["status_code"] or "-"
        latency = f'{result["response_time_ms"]} ms' if result["response_time_ms"] != "" else "-"
        print(f'[{result["status"].upper():10}] {code:>3}  {latency:>10}  {result["url"]}')
        if result["title"]:
            print(f'             title: {result["title"]}')
        if result["error"]:
            print(f'             error: {result["error"]}')


def save_results(results: list[dict], output: str) -> None:
    if output.lower().endswith(".json"):
        with open(output, "w", encoding="utf-8") as file:
            json.dump(results, file, indent=2, ensure_ascii=False)
    elif output.lower().endswith(".csv"):
        fields = [
            "url", "status", "status_code", "title",
            "response_time_ms", "error"
        ]
        with open(output, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(results)
    else:
        raise ValueError("Output file must end with .json or .csv")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check a list of URLs and report their status and response time."
    )
    parser.add_argument(
        "urls",
        nargs="*",
        help="URLs to check directly.",
    )
    parser.add_argument(
        "-f", "--file",
        help="Text file containing one URL per line.",
    )
    parser.add_argument(
        "-o", "--output",
        help="Save results to .json or .csv.",
    )
    parser.add_argument(
        "-t", "--timeout",
        type=float,
        default=10.0,
        help="Request timeout in seconds (default: 10).",
    )
    args = parser.parse_args()

    urls = list(args.urls)
    if args.file:
        urls.extend(read_urls(args.file))

    if not urls:
        parser.error("Provide at least one URL or use --file.")

    results = [check_url(url, args.timeout) for url in urls]
    print_results(results)

    if args.output:
        save_results(results, args.output)
        print(f"\nSaved results to {args.output}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
