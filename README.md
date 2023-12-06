## AI-Serve
*a companion bot capable of understanding different language, voice recognition and displaying emotions

*This project is not for commercial purpose. default character used is Chiaki Nanami from Danganronpa 1

*Hoping to make sth like evil neuro by @vedal987 :) though with inadequate skills 

# Character list:

Chiaki Nanami

<img src="original-size-image/Chiaki Nanami/normal.png">

Celestia Ludenberg

<img src="original-size-image/Celestia Ludenberg/normal.png">

Junko Enoshima

<img src="original-size-image/Junko Enoshima/normal.png">

Kyoko Kirigiri

<img src="original-size-image/Kyoko Kirigiri/normal.png">

- tested environment: python3.9 in debian linux (parrot os)

*install dependencies and run

    python3 -m pip install -r requirements.txt
    python3 -m spacy download en_core_web_sm
    python3 AI-Serve.py

*adjust image size via adjust_image_size.py in emotions/

    <--snip-->
    img.thumbnail((200,200)) <-- edit size here
    <--snip-->
