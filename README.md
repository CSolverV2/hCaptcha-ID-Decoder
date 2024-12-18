# hCaptcha-ID-Decoder
Decode hCaptcha's event id's dynamically, they are not standard like they are in the hsw, they are encoded.

# What Are Event IDs?

These are the IDs hCaptcha uses in theri `hsw` to check if the user is a bot or human

hCaptcha encodes them, making them hard to extract & use easily, so I wrote a decoder/translator

They look like this:
- Encoded -> `14k`
- Translated -> `3666648406`

<img width="479" alt="image" src="https://github.com/user-attachments/assets/95aa1d0e-e419-42fc-beaa-2d26778a4787" />

# How Do We Find Them?

Look in the `hsw.js` for "random" strings like below as an argument to a function

<img width="179" alt="image" src="https://github.com/user-attachments/assets/ce85e8af-998f-4e50-891e-8a0296460f84" />

You can then open `translate.py` to modify the version & encoded id

Run `translate.py` & it will begin to translate the id into the integer format

# Contact

If you need any support or want to purchase anything to help you on your hCaptcha journey please contact me

- [Telegram](https://t.me/CSolverV2)
- [Discord](https://discord.gg/cypa)
