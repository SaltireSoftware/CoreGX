import * as z from 'zod';


/** Options for {@link CoreGx.runCoreGx}. */
export type RunCoreGxOptions = {

  /** A valid CoreGX API key. If not provided, uses the default set on the `CoreGx` instance. */
  apikey?: string;

  /** Random seed to use in model generation. Defaults to a random integer if omitted. */
  seed?: number;

  /** Disable point-location optimization. Defaults to `false`. */
  disableOptimization?: boolean;

  /** Include XML output. Defaults to `true`. */
  xml?: boolean;

  /** Include SVG output. Defaults to `true`. */
  svg?: boolean;

  /** Output equations. Defaults to `true`. */
  equations?: boolean;

  /** ID for this request. */
  requestId?: string;
}

/** Success response from {@link CoreGx.runCoreGx}. */
export type RunCoreGxSuccessValue = {

  /** The generated SVG output. */
  svg?: string;

  /** The generated XML output. */
  xml?: string;

  /** The generated equations output. */
  equations?: string[];

  /** ID for the associated request. */
  requestId?: string;

  /** The random seed for this run. */
  seed: number;
}

export type RunCoreGxSuccess = {

  ok: true;

  value: RunCoreGxSuccessValue;
}

export type CoreGxErrorResponse = {

  ok: false;

  error: string;

};

export type RunCoreGxResponse = RunCoreGxSuccess | CoreGxErrorResponse;

export type GetSyntaxSuccess = {

  ok: true;

  /** A Markdown string describing the CoreGX language. */
  value: string;
}

export type GetSyntaxResponse = GetSyntaxSuccess | CoreGxErrorResponse;

/** Options for initializing a {@link CoreGx} instance. */
export type CoreGxInitOptions = {

  /** Base URL to send CoreGX requests to. If not provided, defaults to `https://api.coregx.dev`. */
  baseUrl?: string;

  /** API key to be passed with requests. If not provided, methods must provide an API key. */
  apiKey?: string;
};

// Decoders
const runCoreGxSuccessSchema: z.ZodType<RunCoreGxSuccess> = z.object({
  ok: z.literal(true),
  value: z.object({
    svg: z.string().optional(),
    seed: z.number(),
    xml: z.string().optional(),
    equations: z.array(z.string()).optional(),
    requestId: z.string().optional(),
  }),
});

const coreGxErrorResponseSchema: z.ZodType<CoreGxErrorResponse> = z.object({
  ok: z.literal(false),
  error: z.string(),
});

const runCoreGxResponseSchema: z.ZodType<RunCoreGxResponse> =
  z.union([
    runCoreGxSuccessSchema,
    coreGxErrorResponseSchema,
  ]);

const getSyntaxSuccessSchema: z.ZodType<GetSyntaxSuccess> = z.object({
  ok: z.literal(true),
  value: z.string(),
});

const getSyntaxResponseSchema: z.ZodType<GetSyntaxResponse> =
  z.union([
    getSyntaxSuccessSchema,
    coreGxErrorResponseSchema,
  ]);

/**
 * Provides an interface to the CoreGX API.
 */
export class CoreGx {

  private baseUrl: string = 'https://api.coregx.dev';
  private apiKey?: string;

  constructor(private options: CoreGxInitOptions = {}) {

    if (options.baseUrl) {
      this.baseUrl = options.baseUrl;
    }

    if (options.apiKey) {
      this.apiKey = options.apiKey;
    }
  }

  private async callApi<T>(endpoint: string, options: { [key: string]: unknown }, responseDecoder: z.ZodType<T>): Promise<T> {
    const address = `${this.baseUrl}/${endpoint}`;
    console.log(address);
    const response = await fetch(address, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(options),
    });
    console.log(response);
    const data = await response.json();
    return responseDecoder.parse(data);
  }

  /**
   * Runs a CoreGX program and returns the response.
   * 
   * See {@link RunCoreGxOptions} for available options.
   */
  public runCoreGx(program: string, options: RunCoreGxOptions = {}): Promise<RunCoreGxResponse> {
    const defaults = { apikey: this.apiKey };
    const params = { program, ...defaults, ...options };
    console.log(params);
    return this.callApi('run-coregx', params, runCoreGxResponseSchema);
  }

  /**
   * Returns the syntax for the CoreGX language.
   */
  public getSyntax(): Promise<GetSyntaxResponse> {
    return this.callApi('get-syntax', {}, getSyntaxResponseSchema);
  }
}
