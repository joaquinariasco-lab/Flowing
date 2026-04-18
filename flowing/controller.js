import Ajv from "ajv";
import addFormats from "ajv-formats";
import { getAIResponse } from "./aiClient.js";

const ajv = new Ajv({ allErrors: true, strict: false });
addFormats(ajv);

/**
 * Validates and enforces schema on AI output.
 * Retries until valid or maxRetries reached.
 * 
 * @param {string} prompt - Original developer prompt
 * @param {object} schema - JSON schema provided by developer
 * @param {string} apiKey - API key
 * @param {number} maxRetries - Max retry attempts
 * @returns {Promise<object>} - Valid structured output
 */
export async function getValidatedAIResponse(
    prompt,
    schema,
    apiKey,
    maxRetries = 3
) {
    const validate = ajv.compile(schema);

    let attempt = 0;
    let lastError = null;

    while (attempt < maxRetries) {
        attempt++;

        try {
            // Force structured output instruction
            const structuredPrompt = `
Return ONLY valid JSON matching this schema:
${JSON.stringify(schema)}

User request:
${prompt}
            `;

            const rawOutput = await getAIResponse(structuredPrompt, apiKey);

            let parsed;

            try {
                parsed = JSON.parse(rawOutput);
            } catch (err) {
                throw new Error("Invalid JSON format");
            }

            const valid = validate(parsed);

            if (valid) {
                return parsed;
            } else {
                lastError = validate.errors;
                console.warn(`Validation failed (attempt ${attempt})`, validate.errors);
            }

        } catch (err) {
            lastError = err.message;
            console.warn(`Attempt ${attempt} failed:`, err.message);
        }
    }

    throw new Error(
        `Failed to generate valid response after ${maxRetries} attempts.\nLast error: ${JSON.stringify(lastError)}`
    );
}
