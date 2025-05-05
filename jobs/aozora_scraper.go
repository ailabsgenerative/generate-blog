package main

import (
	"errors"
	"fmt"
	"io/ioutil"
	"net/http"
	"regexp"
	"strings"

	"golang.org/x/net/html"
)

// GetTxtURLFromHTMLPage extracts the URL of the .txt file from an Aozora Bunko HTML page
func GetTxtURLFromHTMLPage(pageURL string) (string, error) {
	resp, err := http.Get(pageURL)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("failed to fetch page: %s", resp.Status)
	}

	doc, err := html.Parse(resp.Body)
	if err != nil {
		return "", err
	}

	var txtURL string
	var f func(*html.Node)
	f = func(n *html.Node) {
		if n.Type == html.ElementNode && n.Data == "a" {
			for _, attr := range n.Attr {
				if attr.Key == "href" && strings.HasSuffix(attr.Val, ".txt") && !strings.HasPrefix(attr.Val, "http") {
					txtURL = "https://www.aozora.gr.jp" + attr.Val
					return
				}
			}
		}
		for c := n.FirstChild; c != nil; c = c.NextSibling {
			f(c)
		}
	}
	f(doc)

	if txtURL == "" {
		return "", errors.New("no .txt file link found")
	}

	return txtURL, nil
}

// DownloadAozoraTxt downloads the .txt file from the given URL
func DownloadAozoraTxt(txtURL string) (string, error) {
	resp, err := http.Get(txtURL)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("failed to fetch txt file: %s", resp.Status)
	}

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}

	// Assume Shift_JIS encoding
	return string(body), nil
}

// ExtractMainText extracts and cleans the main text from the raw content
func ExtractMainText(text string) (string, error) {
	startMarker := "［＃ここから本文］"
	endMarker := "［＃ここで本文終わり］"

	startIdx := strings.Index(text, startMarker)
	endIdx := strings.Index(text, endMarker)

	if startIdx == -1 || endIdx == -1 {
		return "", errors.New("main text markers not found")
	}

	mainText := text[startIdx+len(startMarker) : endIdx]

	// Remove ruby annotations and other markers
	reRuby := regexp.MustCompile(`《.*?》`)
	reAnnotations := regexp.MustCompile(`［＃.*?］`)
	reVerticalBar := regexp.MustCompile(`｜`)
	reBlankLines := regexp.MustCompile(`\n\n+`)

	mainText = reRuby.ReplaceAllString(mainText, "")
	mainText = reAnnotations.ReplaceAllString(mainText, "")
	mainText = reVerticalBar.ReplaceAllString(mainText, "")
	mainText = reBlankLines.ReplaceAllString(mainText, "\n\n")

	return strings.TrimSpace(mainText), nil
}

func main() {
	// Example: Natsume Soseki's "Kokoro"
	pageURL := "https://www.aozora.gr.jp/cards/000020/files/2569_28291.html"

	// Get the .txt file URL
	txtURL, err := GetTxtURLFromHTMLPage(pageURL)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}
	fmt.Printf("📄 テキストURL: %s\n", txtURL)

	// Download the .txt file
	rawText, err := DownloadAozoraTxt(txtURL)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}

	// Extract and clean the main text
	cleanText, err := ExtractMainText(rawText)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}

	// Display the first 1000 characters of the main text
	fmt.Println(cleanText[:1000])
}