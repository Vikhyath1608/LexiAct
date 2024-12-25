*** Settings ***
Library  BuiltIn

*** Test Cases ***
Context:_play,_classic,_music,
    [Documentation]  Context: play, classic, music, youtube
play a classic music from youtube
