<a href="http://www.wtfpl.net/"><img
       src="http://www.wtfpl.net/wp-content/uploads/2012/12/wtfpl-badge-4.png"
       width="80" height="15" alt="WTFPL" /></a>

# `bip2bib`: map BIP39 words to bible verses

Deterministically map each BIP39 seed word to a Bible verse with optional passphrase.

## Setup

```
git clone https://github.com/cgoliver/bip2bib
cd bip2bib
pip install -r requirements.txt
```

## Usage

```
python bip2bib.py -o out.txt
```

Will generate a text file that looks like:

```
abandon Isaiah 24:8
ability Luke 16:8
able John 10:21
about 2 Chronicles 20:1
above Deuteronomy 5:26
absent Lamentations 3:13
absorb Judges 5:18
...
```

To make the mapping unique (but still deterministic) you can add your own passphrase:

```
python bip2bib.py -o out.txt -p myword
```

Which generates:


```
abandon 2 Corinthians 6:11
ability Psalms 118:102
able Judges 8:4
about Luke 11:32
above Psalms 25:5
absent Leviticus 7:23
absorb 1 John 3:17
...
```

You can always recover this mapping if you remember the seed word you provided.

## How it works

Very simple. We just generate a list of all bible verses in sequential order. The index of each word in the [BIP39 word list](https://github.com/bitcoin/bips/blob/master/bip-0039/english.txt) is hashed with SHA256 to obtain the index of a Bible verse. If you provide a passphrase, the index is hashed together with the passphrase.

> ⚠️ **Warning:** For best reproducibility, make sure you are using `verses.txt` provided in this repository. If you are executing within the cloned repo there should be nothing to do. But if the file is not found in the current directory, a routine will execute to generate a list of all bible verses but it cannot be guaranteed to always be identical since it is generated by a third party library.

> ⚠️ **Warning:** Software provided with no guarantees. Use at your own risk.
