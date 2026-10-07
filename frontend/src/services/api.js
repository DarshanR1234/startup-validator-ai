const API_BASE_URL = 'http://127.0.0.1:8000';

/**
 * Validates a startup idea by sending form parameters to the backend AI agent.
 * @param {Object} params
 * @param {string} params.startup_idea - The detailed startup idea description.
 * @param {string} params.target_country - Target country (e.g., "India").
 * @param {string} params.target_region - Target region (e.g., "Maharashtra").
 * @returns {Promise<Object>} Backend validation result payload.
 */
export async function validateStartupIdea({ startup_idea, target_country, target_region }) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/validate-startup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify({
        startup_idea: startup_idea.trim(),
        target_country: target_country ? target_country.trim() : 'India',
        target_region: target_region ? target_region.trim() : 'Maharashtra',
      }),
    });

    if (!response.ok) {
      let errorMessage = `Server error (${response.status} ${response.statusText})`;
      try {
        const errorData = await response.json();
        if (errorData && errorData.detail) {
          errorMessage = typeof errorData.detail === 'string' 
            ? errorData.detail 
            : JSON.stringify(errorData.detail);
        }
      } catch (e) {
        // Fallback to text parsing if JSON fails
      }
      throw new Error(errorMessage);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      throw new Error(
        'Unable to connect to the backend server at http://127.0.0.1:8000. Please ensure the FastAPI backend is running.'
      );
    }
    throw error;
  }
}
