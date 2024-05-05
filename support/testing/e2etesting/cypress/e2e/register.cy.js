const endpoint = Cypress.config('baseUrl')
const userEmail = 'test'+Date.now()+'@test.com'
const userName = 'test'+Date.now()

describe('register as a user and add prefernences', () => {
  // it('opens homepage', () => {
  //   cy.visit(endpoint)
  // })

  // //click on buton with "sign up"
  // it('opens signup', () => {
  //   cy.visit(endpoint)
  //   cy.contains('Sign Up').debug().click()
  //   cy.url().should('include', '/sign-up')
  //  })

  // it gets redirected to url /sign-up
  it('lets one register', () => {
    /*
    ** First Part - Insert data about one person and click sign up
    */
    cy.visit(endpoint+'/sign-up')
    // in insert data about one person -> email, username, password and password confirmation
    cy.get('input[id="email"]').type(userEmail)
    cy.get('input[id="profile-name"]').type(userName)
    cy.get('input[id="password"]').type('test')
    cy.get('input[id="confirm-password"]').type('test')
    // agree to terms and conditions
    cy.get('input[type="checkbox"]').check()
    // click on submit button
    cy.get('button').contains("Sign Up").click()

    /*
    ** Second Part - Add preferences
    */
    cy.url().should('include', '/onboarding', { timeout: 5000 })
    // add preferences
    const restrictions = ["Vegetarian", "Halal"]
    const preferences = ['Fast Food', 'Japanese', 'Indian', 'Czech', 'Turkish']
    // click on all divs with this text
    for (const restriction of restrictions) {
      cy.contains(restriction).click()
    }

    for (const preference of preferences) {
      cy.contains(preference).click()
    }

    // click on submit button -> wait because is is enabled by state change
    cy.get('button:visible').contains("Next", { timeout: 5000 }).click()
    // assert new url is /
    cy.url().should('eq', endpoint+'/home')
    // there is Hello, userName
    cy.contains('Home')
  })
})