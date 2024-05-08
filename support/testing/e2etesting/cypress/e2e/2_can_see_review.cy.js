const endpoint = Cypress.config('baseUrl')

const secondUser = 'user6'
describe('search a user', () => {
  beforeEach(() => {
      cy.loginByUI('user5', 'user5');
    });

  it('can see others review', () => {
    // I need to ensure that user1 follows user 2 ->ensured by dependency of 1_follow_users.cy.js, this can be improved
    // -> use a seeder to ensure this relatipnship
      cy.visit(endpoint+'/home')
      // now we have to see "user2" on the screen
      cy.contains('user6').should('be.visible')
  })
})