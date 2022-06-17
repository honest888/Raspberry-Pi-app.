
  KioskBoard.Init({

  /*!
  * Required
  * Have to define an Array of Objects for the custom keys. Hint: Each object creates a row element (HTML) on the keyboard.
  * e.g. [{"key":"value"}, {"key":"value"}] => [{"0":"A","1":"B","2":"C"}, {"0":"D","1":"E","2":"F"}]
  */
  keysArrayOfObjects: [
  {
    "0": "Q",
    "1": "W",
    "2": "E",
    "3": "R",
    "4": "T",
    "5": "Y",
    "6": "U",
    "7": "I",
    "8": "O",
    "9": "P"
  },
  {
    "0": "A",
    "1": "S",
    "2": "D",
    "3": "F",
    "4": "G",
    "5": "H",
    "6": "J",
    "7": "K",
    "8": "L"
  },
  {
    "0": "Z",
    "1": "X",
    "2": "C",
    "3": "V",
    "4": "B",
    "5": "N",
    "6": "M"
  }
],

  /*!
  * Required only if "keysArrayOfObjects" is "null".
  * The path of the "kioskboard-keys-${langugage}.json" file must be set to the "keysJsonUrl" option. (XMLHttpRequest to getting the keys from JSON file.)
  * e.g. '/Content/Plugins/KioskBoard/https://www.cssscript.com/demo/virtual-keyboard-numpad-kioskboard/dist/kioskboard-keys-english.json'
  */
  //keysJsonUrl: 'kioskboard-keys-english.json',

  /*
  * Optional: (Special Characters Object)* Can override default special characters object with the new/custom one.
  * e.g. {"key":"value", "key":"value", ...} => {"0":"#", "1":"$", "2":"%", "3":"+", "4":"-", "5":"*"}
  */
  specialCharactersObject: null,

  // Optional: (Other Options)

  // Language Code (ISO 639-1) for custom keys (for language support) => e.g. "en" || "tr" || "es" || "de" || "fr" etc.
  language: 'en',

  // The theme of keyboard => "light" || "dark" || "flat" || "material" || "oldschool"
  theme: 'light',

  // Uppercase or lowercase to start. Uppercase when "true"
  capsLockActive: true,

  // Allow or prevent real/physical keyboard usage. Prevented when "false"
  allowRealKeyboard: false,

  // CSS animations for opening or closing the keyboard
  cssAnimations: true,

  // CSS animations duration as millisecond
  cssAnimationsDuration: 360,

  // CSS animations style for opening or closing the keyboard => "slide" || "fade"
  cssAnimationsStyle: 'slide',

  // Allow or deny Spacebar on the keyboard. The keyboard is denied when "false"
  keysAllowSpacebar: true,

  // Text of the space key (spacebar). Without text => " "
  keysSpacebarText: 'Space',

  // Font family of the keys
  keysFontFamily: 'sans-serif',

  // Font size of the keys
  keysFontSize: '22px',

  // Font weight of the keys
  keysFontWeight: 'normal',

  // Size of the icon keys
  keysIconSize: '25px',

});


// Run KioskBoard
// Select any input or textarea element(s) to run KioskBoard
KioskBoard.Run('.virtual-keyboard');
 
