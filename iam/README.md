`temp-rebuild-read.json` is temporary. Attach it to the Lambda role only while
running the `rebuild_from_raw` event, then delete it. The normal role is
write-only (`lambda-inline-policy.json`).