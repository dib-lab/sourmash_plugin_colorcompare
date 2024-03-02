

# sourmash_plugin_colorcompare
The color_compare plugin takes the output matrix file from sourmash compare (similarity matrix, csv) and plots a similarity heatmap of the signatures, with on the y-axis colors that correspond to an arbitrary category set by the categories csv, which is the other input file. 

Examples of these categories could be:
1. Phylogenetic information of the signature (e.g. family/genus/species)
2. Environment that the sequence the sig file was made from originated (e.g. marine, soil, gut)
3. Treatment of samples that were used to create sig files (if using metagenome reads)

## Installation

```
pip install git+https://github.com/dib-lab/sourmash_plugin_colorcompare.git
```

## Usage

```
sourmash scripts color_compare similarity_matrix.csv categories.csv -o output.png 
```

## Support

We suggest filing issues in [the main sourmash issue tracker](https://github.com/dib-lab/sourmash/issues) as that receives more attention!

## Dev docs

`xyz` is developed at https://github.com/sourmash-bio/sourmash_plugin_template.

### Generating a release

Bump version number in `pyproject.toml` and push.

Make a new release on github.

Then pull, and:

```
python -m build
```

followed by `twine upload dist/...`.
