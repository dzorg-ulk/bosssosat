import json
import requests

def ask_qwen(prompt, base_url="http://localhost:11434"):
    try:
        response = requests.post(
            f"{base_url}/api/generate",
            json={
                "model": "qwen2:1.5b",
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )

        if response.status_code == 200:
            return response.json().get("response", "")
        else:
            return f"Ошибка сервера: {response.status_code}"

    except requests.exceptions.ConnectionError:
        return "Не удалось подключиться к Ollama. Надо запустить сервер: ollama serve"
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"


def load_artifacts():
    with open('artifacts.json', 'r', encoding='utf-8') as f:
        artifacts = json.load(f)

    return artifacts

def clear_artifacts(artifacts, type):
    artifacts[type] = []

    answer = ask_qwen(
        f"""
        Сгенерируй ОДИН случайный артефакт не больше двух слов для игры "Студент: Возвращение в родной город". Игра - текстовая RPG про студента, вернувшегося в родной город на каникулы. Артефакт должен быть реалистичным, связанным с ностальгией, детством, друзьями, родителями или студенческой жизнью. 

        Формат ответа только слово без комментариев и знаков препинания в именительном падеже: "Название артефакта",

        Тема артефакта {type}: 
        """)

    artifacts[type] = [answer]

    print(answer)

    with open('artifacts.json', 'w', encoding='utf-8') as f:
        json.dump(artifacts, f, ensure_ascii=False, indent=4)

clear_artifacts(load_artifacts(), "Чаепитие")


