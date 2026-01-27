import Ajv, { type ValidateFunction } from 'ajv';

const ajv = new Ajv({
  allErrors: true,
  strict: false,
});

const validatorCache = new Map<string, ValidateFunction>();

export function validateOrThrow<T>(
  schemaName: string,
  schema: object,
  data: unknown
): T {
  let validate = validatorCache.get(schemaName);
  if (!validate) {
    validate = ajv.compile(schema);
    validatorCache.set(schemaName, validate);
  }

  const valid = validate(data);
  if (!valid) {
    const message = ajv.errorsText(validate.errors, { separator: '; ' });
    const error = new Error(
      `Schema validation failed for ${schemaName}: ${message}`
    );
    (error as Error & { errors?: unknown }).errors = validate.errors || [];
    throw error;
  }

  return data as T;
}
