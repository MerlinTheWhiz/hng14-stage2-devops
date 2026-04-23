// ESLint v9 flat config — CommonJS, no external imports required
module.exports = [
  {
    files: ["**/*.js"],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: "commonjs",
      globals: {
        require: "readonly",
        module: "readonly",
        exports: "readonly",
        __dirname: "readonly",
        __filename: "readonly",
        process: "readonly",
        console: "readonly",
      },
    },
    rules: {
      "no-undef": "error",
      "no-unused-vars": "warn",
      "no-console": "off",
    },
  },
];
