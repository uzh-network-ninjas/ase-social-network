const endpoint = Cypress.config('baseUrl')

const secondUser = 'user6'
describe('search a user', () => {
  beforeEach(() => {
      cy.loginByUI('user5', 'user');
    });

  it('can see others review', () => {
      // now we have to see "user2" on the screen
      cy.contains('user6').should('be.visible')

  })
})