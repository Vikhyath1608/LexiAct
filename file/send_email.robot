*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${BROWSER}    Chrome
${SEARCH_ENGINE_URL}    https://www.google.com
${SEARCH_QUERY}    Robot Framework Tutorial

*** Test Cases ***
Open Browser And Search Content
    [Documentation]    This test case opens a browser, navigates to a search engine, and searches for specific content.
    Open Browser    ${SEARCH_ENGINE_URL}    ${BROWSER}
    Input Text    name=q    ${SEARCH_QUERY}
    Press Keys    name=q    ENTER
    Wait Until Page Contains    ${SEARCH_QUERY}    timeout=10s
    Take Screenshot
    Close Browser