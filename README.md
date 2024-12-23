# mkt-sentiment-strat
Algorithm to track market sentiment on Reddit to inform active investment strategy.

## Description
As part of our Applied Investment Managemnt course (FINE 541) offered at McGill University, our team devised an active investment strategy with the goal of generating alpha for our endowment fund of $200,000 CAD. This involved developing a trading algorithm in Python to scrape Reddit data for sentiment intensity analysis, leveraging the VADER NLP model to produce buy and sell signals. We also conducted comprehensive backtests to validate and enhance the strategy’s performance.

## Authors
Christopher Smith

## Getting Started
1. Clone the repository: $ git clone https://github.com/Chris-Smith22/mkt-sentiment-strat
2. Setup virtual environment:
    - $ python -m venv .venv
    - $ source .venv/bin/activate
3. Install dependencies from requirements.txt: pip install -r requirements.txt
4. Follow Reddit App setup instructions detailed in api_process.md
5. Create a file"./docs/dev_settings.py" and set CLIENT_ID, CLIENT_SECRET and USER_AGENT fields.

## Helpful Links
NLTK VADER model: https://www.nltk.org/_modules/nltk/sentiment/vader.html
FINE 541: https://www.mcgill.ca/study/2024-2025/courses/fine-541n1

## License
This project is licensed under the MIT License
