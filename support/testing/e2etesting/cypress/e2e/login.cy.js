const endpoint = "/"
const userEmail = 'user1@uzh.ch'
const userPassword = 'user'
const userName = 'user1'

describe('login as a user', () => {

  // register as a seeded user
  it('lets one login', () => {
    cy.visit(endpoint)
    cy.contains('Sign In').click()
    cy.url().should('include', '/sign-in')

    cy.get('input[id="profile-name"]').type(userName)
    cy.get('input[id="password"]').type(userPassword)

    cy.get('button').contains("Sign In").click()

    // redirect to / -> sometimes we get redirected to /onboarding, redirect back manually

    cy.url().should('not.eq', Cypress.config('baseUrl')+"/sign-in") // kinda a workload ->wait for redirect doesn't matter to what
+
    cy.visit('/home')
    cy.contains('Home')
    // now we open preferences, because the user was seeded
  })
})