# Flask Wordle

To be update.

## TL;DR

Make sure you have conda/mamba and node/nvm installed, and run:

```bash
bash node.sh
mamba env create
mamba activate wordle
python webapp.py
```

The application should be running at port 5000.

## List of dependencies

<details> <!-- markdownlint-disable-line MD033 -->

[package.json]: package.json
[environment.yml]: environment.yml

### Python dependencies

|Package            |Version        |Channel        |Settings         |Remarks                |
|:------------------|:--------------|:--------------|:----------------|:---------------------:|
|python             |>=3.12.0       |conda-forge    |[environment.yml]|                       |
|flask              |>=3.0          |conda-forge    |[environment.yml]|                       |
|waitress           |>=3.0          |conda-forge    |[environment.yml]|                       |

### Javascript dependencies

|Package            |Version        |Channel        |Settings         |Remarks                |
|:------------------|:--------------|:--------------|:----------------|:---------------------:|
|typescript         |>=5.5          |npm            |[package.json]   |                       |
|sass               |>=1.77         |npm            |[package.json]   |                       |
|webpack            |>=5.93         |npm            |[package.json]   |                       |

</details>

## Install Python dependencies

- Install [miniconda](docs/miniconda.md) if needed
- Install [mamba](docs/mamba.md) if needed

### A. With YAML configuration

```bash
mamba env create                            # For production
mamba env create -f environment.dev.yml     # For development
mamba activate wordle
```

### B. With CLI

<details> <!-- markdownlint-disable-line MD033 -->

```bash
mamba create -n wordle
mamba activate wordle

mamba install -c conda-forge flask cython waitress -y
mamba install -c conda-forge regex -y

# Dev dependencies
mamba install -c conda-forge ipykernel djlint ruff -y
```

</details>

## Install Javascript dependencies

- Install [nvm](docs/node.md) if needed

### Automatically config and generate js and css

```bash
bash node.sh
```

### Manually config nvm and node

```bash
nvm install
nvm use

npm install
```

## Webpack

```bash
npm run webpack                 # In production mode or
npm run webpack:watch           # In debug mode
```

## Ruff

```bash
ruff check .                # Check mode
ruff check . --watch        # Watch mode
```

## Run the app

```bash
python webapp.py            # In production mode or
python webapp.py --flask    # In flask mode or
python webapp.py --debug    # In debug mode
```
