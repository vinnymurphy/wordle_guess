# wordle_guess

We look at all the words in the dictionary and determine what letters are the most used.  An issue with using the words from the unix is they are not the words used by NY Times.

Another issue with just looking at the letters we can not determine what words are used the most.  Once we get down to a managable set of
words we sort by how often a word is using ./big.txt

big.txt comes from the Natural Language Corpus Data.  I'm not convinced this is the best probability of words, but it is a perfect approximation of words in the English language.

## Key Features

* Choose wordle words
* Cross platform
  - macOS and Linux ready.

## How To Use

To clone and run this application.  You'll need a recent version of python.  The walrus operator is used, so python needs to be at least 3.8

```bash
# Clone this repository
$ git clone https://github.com/vinnymurphy/wordle_guess.git

# Go into the repository
$ ./wordle

```

## Hack

The algorithm that wordle uses is very smart in that it picks words with multiple options to chose.  Words like arise, raise, et cetra have a very high character level probability. The algorithm seems to know these high probability words and picks words that are not the five characters a, e, i, r, s.

If you're logged into wordle and close to being incorrect 6 times use another browser to get a non-logged in [wordle](https://www.nytimes.com/games/wordle/index.html) window.  Using a Chrome browser as your primary logged in account you can use any of these other browsers to guess non-logged in choices.  

Non-Chrome browsers:

- [Opera](https://www.opera.com/)
- [Safari](https://www.apple.com/safari/)
- [Tor](https://www.torproject.org/download/)
- [Brave](https://brave.com/)
- [Edge](https://www.microsoft.com/en-us/edge/download)

The reason you'll need another browser is because [wordle](https://www.nytimes.com/games/wordle/index.html) uses [cookies](https://www.w3schools.com/js/js_cookies.asp) to cache your guesses.  

## Credits

This software uses the following open source packages:

- [Wordle Solving](https://www.inspiredpython.com/article/solving-wordle-puzzles-with-basic-python)
- [Natural Language Corpus Data](https://norvig.com/ngrams/)


## License

MIT

