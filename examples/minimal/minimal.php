#!/usr/bin/env php
<?php
// Minimal working example: CoreGX source to SVG.
//
// Usage:
//   COREGX_API_KEY=your-key ./minimal.php < example.coregx > output.svg

$program = stream_get_contents(STDIN);

$context = stream_context_create([
    "http" => [
        "method" => "POST",
        "header" => "Content-Type: application/json",
        "content" => json_encode([
            "apikey" => getenv("COREGX_API_KEY"),
            "program" => $program,
            "svg" => true,
        ]),
        "ignore_errors" => true,
    ],
]);
$response = file_get_contents("https://api.coregx.dev/run-coregx", false, $context);

$result = json_decode($response, true);

if (!$result["ok"]) {
    fwrite(STDERR, "CoreGX error: {$result['error']}\n");
    exit(1);
}

echo $result["value"]["svg"] . "\n";
