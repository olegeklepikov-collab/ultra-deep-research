# Contributing / Участие в разработке

[English overview](README.md) · [Русское описание](README.ru.md)

## English

This repository publishes installable runtime snapshots and their documentation. The private/operator deployment state and the full historical qualification workbench are not part of the release archive. Do not assume an unlisted CI pipeline or a complete benchmark runner is available in this checkout.

For an issue, include the exact release tag/commit, affected tool or script, a minimal sanitized input, expected and observed behavior, and the relevant status or receipt field. Preserve a failed attempt before proposing a retry. Never post credentials, private source documents, raw auth stores, or unrestricted runtime logs.

For a change, use a focused branch and pull request. Describe the behavior being corrected, affected contract fields, compatibility impact, and the smallest meaningful regression evidence. Test the changed boundary and one relevant failure case; do not rerun or redesign unrelated workflows solely to increase a test count. Never turn a supplied assertion into verified evidence or remove a failed gate to obtain a success label.

Keep English and Russian documentation aligned. Code identifiers and exact statuses stay unchanged in translation. When documenting a release, use its immutable source ref, real artifact checksums and observed scope. Do not rewrite signed artifacts or move a published tag to update prose; update documentation or issue a new artifact version.

## Русский

Репозиторий публикует устанавливаемые снимки исполняемого кода и документацию. Частное состояние развёртывания и полный исторический стенд квалификации не входят в архив выпуска. Не следует предполагать наличие неуказанной системы CI или полного средства исполнения эталонных испытаний в этой копии.

В сообщении о проблеме укажите точные тег/коммит, инструмент или сценарий, минимальный очищенный вход, ожидаемое и фактическое поведение, соответствующий статус или поле квитанции. Сохраните неудачную попытку до предложения повтора. Не публикуйте реквизиты, закрытые источники, файлы авторизации или неограниченные журналы среды.

Изменения оформляются узкой веткой и запросом на включение. Опишите исправляемое поведение, поля контракта, совместимость и минимальную содержательную регрессионную проверку. Проверьте затронутую границу и один существенный отказ; не перепроектируйте и не повторяйте несвязанные процессы ради числа тестов. Нельзя превращать переданную декларацию в подтверждение или удалять неуспешную проверку ради ярлыка успеха.

Поддерживайте согласованность английского и русского текстов. Идентификаторы кода и точные статусы при переводе не меняются. Для выпуска используйте неизменяемую ссылку на исходники, реальные хеши и наблюдённую область. Изменение описания не требует переписывания подписанного архива или переноса опубликованного тега: обновляйте документацию либо выпускайте новую версию артефакта.
