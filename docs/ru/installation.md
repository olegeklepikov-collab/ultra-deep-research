# Установка и настройка

[Главная](../../README.ru.md) · [English](../en/installation.md)

> Эти шаги воспроизводят подписанный r152. Выбор класса модели в текущей разработке описан отдельно: [классы моделей](model-classes.md).

## Выберите состав развёртывания

Research предоставляет локальные контрактные инструменты и ограниченные исследовательские сценарии. Полная управляемая среда дополнительно требует Foundation и его служб состояния. Установка расширения не разворачивает эти службы и не авторизует модель.

Исходные пакеты требуют Python 3.11 или новее. Стенд выпуска использовал Python 3.13 на macOS с Docker. Foundation закрепляет Hermes 0.21.3, коммит `2034126e0d1f397b4612782156097243dbbdc819`, и включённую поправку авторизации кнопок Telegram. Для воспроизведения выпуска недостаточно произвольной сборки Hermes с похожим номером версии.

| Возможность | Необходимые компоненты |
|---|---|
| Исследовательские контракты | Совместимый Hermes, загрузчик расширений и зависимости из `plugin.yaml` |
| Процессы с моделью | Разрешённый поддержанный модельный маршрут; Python и `venv/bin/hermes` из одного окружения |
| Ограниченное получение веб-источников | Приведённая ниже настройка только Keenable и исходящий HTTPS |
| Изучение PDF | `pdfplumber==0.11.9`; для соответствующих сценариев также `psutil`, `anydoc`, `pdfinfo`, `pdftoppm`/Poppler |
| Службы Foundation | Git, Beads, Dolt, Docker, age и Minisign согласно руководствам компонентов и закреплённым манифестам |

Установщик расширений Hermes показывает зависимости Python, но не устанавливает их автоматически. Установите объявленные пакеты в фактическое окружение Hermes. Ограничение ресурсов разборщика не заменяет изоляцию недоверенных документов.

## Получение и проверка

Используйте пустой каталог. Опубликованный архив неизменяем; хеши относятся к нему, а не к обновляемой документации.

```sh
mkdir udr-r152-v21
cd udr-r152-v21
gh release download v0.41.0a1-r152-v21   --repo olegeklepikov-collab/ultra-deep-research   --pattern hermes-local-release-r152-v21.zip
printf '%s  %s\n'   02c5032a8626d7a5ca782b78067530de83fe808a413dbbdf373850620e2cf334   hermes-local-release-r152-v21.zip | shasum -a 256 -c -
unzip hermes-local-release-r152-v21.zip
minisign -Vm foundation.zip -p release-signing.pub
```

`manifest.json` содержит хеши компонентов. Отпечаток доверенного открытого ключа SHA-256: `2295aaab3cb418c4f81a867a701a8187e8cdd0f73105a1f318c1faf981dfdb1a`. Сверьте `research.zip` с `research_report.bundle_sha256` в `bridge-lock.json` внутри проверенного архива Foundation. Так подтверждается согласованность компонентов. Для внешнего ZIP опубликован хеш; подпись Foundation находится внутри него.

## Установка Research в новый экземпляр

Выберите и подготовьте новый домашний каталог штатной настройкой Hermes. Переменные ниже должны указывать именно на него. Затем установите точный коммит выпуска:

```sh
export HERMES_HOME="$HOME/.hermes-udr"
export HERMES_FOUNDATION_ROOT="$HERMES_HOME/foundation"
hermes plugins install olegeklepikov-collab/ultra-deep-research   --ref 9077d24d5e7b6dda5db7902bac2a927503791db6 --no-enable
hermes plugins doctor ultra-deep-research --ci
hermes plugins enable ultra-deep-research --no-allow-tool-override
```

Тег выпуска — `v0.41.0a1-r152-v21`. Полный коммит однозначно задаёт устанавливаемые исходники; основная ветка не является идентификатором этой поставки.

## Авторизация и выбор модели

Отдельная OAuth-сессия Codex создаётся в выбранном домашнем каталоге:

```sh
hermes auth add openai-codex --type oauth --label "UDR workstation"
```

Выполните инструкции входа по коду, затем добавьте настройки модели и источников в `config.yaml` этого экземпляра. Авторизация сама по себе не выбирает модельный маршрут.

```yaml
model:
  provider: openai-codex
  default: gpt-5.6-sol

web:
  search_backend: keenable
  extract_backend: keenable
  keyless_rescue: false
  provider_tier:
    keenable: free
    exa: paid
    parallel: paid
    firecrawl: paid
```

Три значения `paid` исключают этих поставщиков из цепочки резервных обращений без ключей. Ограниченный процесс выбирает только Keenable и отключает резервное переключение. Такая настройка не создаёт учётные данные и не разрешает платные обращения к остальным поставщикам.

Второй поддержанный ограниченный маршрут — `openrouter` с `openai/gpt-5.4-nano` и реквизитами OpenRouter, предоставленными оператором. Другие пары не принимаются автоматически ограниченным модельным обработчиком этой версии. Для него нужно отключить `fallback_model` и `fallback_providers`. Не меняйте настройки посреди запуска: перед следующими действиями проверяется их отпечаток.

OAuth-реквизиты остаются в закрытом хранилище выбранного домашнего каталога и не включаются в репозиторий. Запись `included` с нулевой оценкой отдельного вызова описывает подписочный учёт, а не отсутствие экономической стоимости всей работы.

## Подключение Foundation

После проверки архива следующий пример создаёт локальный Git-источник ровно из перечисленных в его манифесте файлов. Предварительно настройте собственную личность автора Git. Коммит локальной установки отличается от исходного коммита Foundation, указанного в подписанном манифесте.

```sh
unzip foundation.zip -d foundation-source
python3 - <<'PYCODE'
import json
import subprocess
from pathlib import Path
root = Path("foundation-source").resolve()
manifest = json.loads((root / "bundle-manifest.json").read_text())
files = [row["path"] for row in manifest["files"]] + ["bundle-manifest.json"]
subprocess.run(["git", "-C", str(root), "init", "-b", "release"], check=True)
subprocess.run(["git", "-C", str(root), "add", "--", *files], check=True)
subprocess.run(["git", "-C", str(root), "commit", "-m", "Exact Foundation v21 package"], check=True)
PYCODE
UDR_FOUNDATION_REF="$(git -C foundation-source rev-parse HEAD)"
hermes plugins install "file://$PWD/foundation-source" \
  --ref "$UDR_FOUNDATION_REF" --no-enable
hermes plugins doctor hermes-foundation-bridge --ci
hermes plugins enable hermes-foundation-bridge --no-allow-tool-override
```

Перед управляемыми операциями выполните инструкции `README.md`, `RELEASE.md`, `DOLT_SQL.md`, `RECOVERY.md` из архива:

1. Создайте новую копию исходников коммита Hermes из `bridge-lock.json`; примените включённую поправку в этой копии после проверки исходного хеша и `git apply --check`. Проверьте хеш исправленного файла Telegram.
2. Создайте новые каталоги Foundation, профили, служебные идентификаторы, сети и тома Docker, локальные реквизиты. Подготовьте закреплённые компоненты SQL, памяти, графа и поиска.
3. Сначала вызовите `foundation_bridge_migrate` с `apply=false`. Применяйте миграции только к выбранному новому каталогу, затем подготовьте необходимые профили, индекс, граф, память и Beads.
4. Поместите ZIP Foundation, подпись и открытый ключ в `HERMES_FOUNDATION_ROOT/releases/hermes-foundation-bridge-0.12.0/` под именами из руководства выпуска. Вызовите `foundation_release_verify` с версией `0.12.0` и коммитом `a3305205a77ac7a10abbb7692076090106132559`.
5. Изучите `foundation_bridge_health`, завершите применимые проверки экземпляра и зафиксируйте отдельное решение оператора об активации. Включение расширения регистрирует инструменты, но не активирует производство.

Это явные шаги развёртывания. Общий ZIP не является автоматическим установщиком или резервной копией рабочей среды автора.

## Обновление и откат

До обновления сохраните текущий точный коммит и проверенный архив. Отключите затронутое расширение, установите новый точный ref с `--force --no-enable`, выполните doctor и необходимые характерные проверки; включайте только после успешного решения. Для отката установите сохранённый прежний ref тем же публичным механизмом.

Сохраняйте согласованность Research и Foundation. Откат кода не восстанавливает изменённые базы и не оправдывает удаление новых записей: данные восстанавливаются по отдельному контракту. Изменённый архив требует собственной подписи.
