async function startTranslation() {
  const sourceLang = document.getElementById("sourceLang").value;
  const targetLang = document.getElementById("targetLang").value;

  document.getElementById("recognized").innerText = "Listening...";
  document.getElementById("translated").innerText = "";

  const res = await fetch("/translate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ source: sourceLang, target: targetLang })
  });

  const data = await res.json();
  if (data.error) {
    alert(data.error);
  } else {
    document.getElementById("recognized").innerText = data.recognized;
    document.getElementById("translated").innerText = data.translated;
  }
}



// document.addEventListener("DOMContentLoaded", () => {
//   const micBtn = document.getElementById("micBtn");
//   const sourceLang = document.getElementById("sourceLang");
//   const targetLang = document.getElementById("targetLang");
//   const recognizedDiv = document.getElementById("recognized");
//   const translatedDiv = document.getElementById("translated");

//   micBtn.addEventListener("click", async () => {
//     micBtn.disabled = true;
//     micBtn.innerText = "🎙️ Listening...";

//     try {
//       const response = await fetch("/translate", {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json"
//         },
//         body: JSON.stringify({
//           source_lang: sourceLang.value,
//           target_lang: targetLang.value
//         })
//       });

//       const data = await response.json();

//       if (data.error) {
//         recognizedDiv.innerHTML = `🛑 Error: ${data.error}`;
//         translatedDiv.innerHTML = "";
//       } else {
//         recognizedDiv.innerHTML = `🗣️ Recognized: ${data.recognized}`;
//         translatedDiv.innerHTML = `🌍 Translated: ${data.translated}`;
//       }

//     } catch (err) {
//       recognizedDiv.innerHTML = `⚠️ Error: ${err.message}`;
//       translatedDiv.innerHTML = "";
//     }

//     micBtn.disabled = false;
//     micBtn.innerText = "🎙️ Start Talking";
//   });
// });

  