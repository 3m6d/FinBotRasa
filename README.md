## Introduction

FinBotRasa is a financial bot built using the Rasa framework. This project aims to provide automated text and voice-based conversations for financial services.

## Features

- **Automated Conversations**: Supports text interactions.
- **Contextual Understanding**: Capable of layered conversations with context.

## Installation

### Prerequisites

- Python 3.6 or higher
- Pip package manager

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/3m6d/FinBotRasa.git
   cd FinBotRasa
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Train the model:
   ```bash
   rasa train
   ```

2. Run the action server:
   ```bash
   rasa run actions
   ```

3. Start the Rasa server:
   ```bash
   rasa shell
   ```

## Debugging

To debug the action server, use:
```bash
rasa run actions --debug
```

To learn how the bot is working interactively, use:
```bash
rasa interactive
```

To debug interactive mode, use:
```bash
rasa interactive --debug
```

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Links

- [Rasa Documentation](https://rasa.com/docs)
- [Rasa Community Forum](https://forum.rasa.com)
- [Rasa GitHub](https://github.com/RasaHQ/rasa)

For more information, you can refer to the [original README](https://github.com/3m6d/FinBotRasa/blob/main/README.md).
