# UwUMaths

## Contents

-   [Requirements](#requirements)
-   [Communication](#communication)
-   [Installation from source](#installation-from-source)
-   [Using the application](#using-the-application)
-   [Credits](#credits)
-   [License](#license)

## Requirements

-   Python3
-   Pandas

## Communication

-   If you have a bug or an issue, please contact us.

## Installation from source

### SSH

```bash
git clone git@github.com:EpitechPromo2026/B-CNA-500-TLS-5-1-neuralnetwork-baptiste.laran.git
```

## Dataset

To download dataset :

```bash
wget http://labourel.ddns.net/data_train.csv
wget http://labourel.ddns.net/data_test.csv
```

or just use the URL in the binaries as dataset path.

## Format

The dataset must be a CSV file with at least the following fields :

```csv
"RES";"FEN"
"white", <fen>
"black", <fen>
"pat", <fen>
```

## Using the binaries

### Trainer

To train the neural network, you can use the trainer binary.

```bash
./trainer -h
```

### Loader

The loader binary is used to load a trained neural network and use it to predict a value.

```bash
./loader -h
```

## Credits

-   Baptiste Laran
-   Maxence Labourel

## License

UwUMaths is developped by the UwUClub for Epitech.
