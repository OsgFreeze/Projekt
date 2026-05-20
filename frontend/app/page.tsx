"use client"

import { useState } from "react"

export default function HomePage() {
  const [inputText, setInputText] = useState("")
  const [outputText, setOutputText] = useState("")
  const [loading, setLoading] = useState(false)

  const handleImprov = async () => {
    //if (!inputText.trim()) return

    setLoading(true)

    try {
      const response = await fetch("http://127.0.0.1:8000/api/process", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: inputText
        }),
      })

      if (!response.ok){
        throw new Error("Fehler beim Senden an das Backend")
      }

      const data = await response.json()
      setOutputText(data.cleaned_text)

    } catch (error){
      console.error(error)
      setOutputText("Fehler: Backend nicht erreichbar oder Antwort ungültig.")
    } finally {
      setLoading(false)
    }
  }

  const handleCopy = async () => {
    if (!outputText) return

    try {
      await navigator.clipboard.writeText(outputText)
    } catch (error) {
      console.error("Kopieren fehlgeschlagen:", error)
    }
  }

  return (
    <main className="page">
      <section className="blocksWrapper">
        <div className="blockColumn">
          <textarea
            className="textBlock inputBlock"
            placeholder="Eingabe"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
          />
          <button
            className="actionButton"
            onClick={handleImprov}
            disabled={loading}
          >
            {loading ? "Lädt..." : "Verbessern"}
          </button>
        </div>

        <div className="blockColumn">
          <div className="textBlock outputBlock">
            {outputText || "Ausgabe"}
          </div>
          <button className="actionButton" onClick={handleCopy}>
            Copy
          </button>
        </div>
      </section>
    </main>
  )
}
