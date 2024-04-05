import apiClient from '@/services/axios'

export const authService = {
  async signUp(email: string, username: string, password: string) {
    await apiClient.post('/authenticator/user', {
      username: username,
      email: email,
      password: password
    })
  },

  async signIn(username: string, password: string): Promise<string> {
    const response = await apiClient.post('/authenticator/token', {
      username: username,
      password: password
    })

    if (response.data?.['access_token'] === undefined) {
      throw new Error('Sign in response did not include an access token.')
    }
    return response.data['access_token']
  },

  async updatePassword(currentPassword: string, newPassword: string) {
    await apiClient.patch('/authenticator/password', {
      curr_password: currentPassword,
      new_password: newPassword
    })
  }
}
