import pygame

from ui import theme


class ParticleView:

    def draw(self, surface, particle, rect, t):

        # ----------------------------
        # Layout
        # ----------------------------

        panel = self.layout_panel(rect)

        content = self.layout_content(panel)

        animation = self.layout_animation_rect(content)

        cards = self.layout_cards_rect(content, animation)

        description = self.layout_description_rect(content, cards)

        # ----------------------------
        # Renderização
        # ----------------------------

        self.draw_panel(surface, particle, panel)

        self.draw_animation(surface, particle, animation, t)

        self.draw_cards(surface, particle, cards)

        self.draw_description(surface, particle, description)

    # =====================================================
    # LAYOUT
    # =====================================================

    def layout_panel(self, rect):
        return rect

    def layout_content(self, panel):

        padding = 30

        return panel.inflate(
            -padding * 2,
            -padding * 2,
        )

    def layout_animation_rect(self, content):

        height = int(content.height * 0.35)

        return pygame.Rect(
            content.x,
            content.y,
            content.width,
            height,
        )

    def layout_cards_rect(self, content, animation):

        spacing = 20
        height = 120

        return pygame.Rect(
            content.x,
            animation.bottom + spacing,
            content.width,
            height,
        )

    def layout_description_rect(self, content, cards):

        spacing = 20

        return pygame.Rect(
            content.x,
            cards.bottom + spacing,
            content.width,
            content.bottom - cards.bottom - spacing,
        )

    # =====================================================
    # DRAW
    # =====================================================

    def draw_panel(self, surface, particle, panel):

        pygame.draw.rect(
            surface,
            theme.PANEL_BG,
            panel,
            border_radius=18,
        )

        pygame.draw.rect(
            surface,
            particle["color"],
            panel,
            2,
            border_radius=18,
        )

        sidebar = pygame.Rect(
            panel.x,
            panel.y,
            8,
            panel.height,
        )

        pygame.draw.rect(
            surface,
            particle["color"],
            sidebar,
            border_radius=4,
        )

    def draw_animation(self, surface, particle, rect, t):

        cx = rect.centerx
        cy = rect.centery

        match particle["name"]:

            case "Elétron":
                self.draw_electron(surface, cx, cy, t)

            case "Quark Up":
                self.draw_quark_up(surface, cx, cy, t)

            case "Quark Down":
                self.draw_quark_down(surface, cx, cy, t)

            case "Fóton":
                self.draw_photon(surface, cx, cy, t)

            case "Neutrino":
                self.draw_neutrino(surface, cx, cy, t)

            case "Glúon":
                self.draw_gluon(surface, cx, cy, t)

            case "Pósitron":
                self.draw_positron(surface, cx, cy, t)

            case "Bóson de Higgs":
                self.draw_higgs(surface, cx, cy, t)
        
    def draw_electron(self, surface, x, y, t):

        pygame.draw.circle(surface, (255,120,120), (x,y), 12)

        pygame.draw.circle(surface, theme.WHITE, (x,y), 60, 2)

        angle = t*2

        ex = x + math.cos(angle)*60
        ey = y + math.sin(angle)*60

        pygame.draw.circle(
            surface,
            (0,255,255),
            (int(ex), int(ey)),
            8
        )
        
    def draw_quark_up(self, surface, x, y, t):

        r = 35

        for i, color in enumerate([
            (255,0,0),
            (0,255,0),
            (0,150,255)
        ]):

            a = t + i*2.09

            px = x + math.cos(a)*r
            py = y + math.sin(a)*r

            pygame.draw.circle(surface,color,(int(px),int(py)),12)

        pygame.draw.circle(surface,theme.WHITE,(x,y),45,2)
    def draw_quark_down(self, surface, x, y, t):

        r = 25

        for i in range(3):

            a = -t+i*2.09

            px = x+math.cos(a)*r
            py = y+math.sin(a)*r

            pygame.draw.circle(
                surface,
                (255,255,0),
                (int(px),int(py)),
                10
            )        
    
    def draw_photon(self, surface, x, y, t):

        pts=[]

        for i in range(140):

            xx=x-70+i

            yy=y+math.sin(i/12+t*5)*12

            pts.append((xx,yy))

        pygame.draw.lines(
            surface,
            (255,220,0),
            False,
            pts,
            4
        )
    
    def draw_neutrino(self, surface, x, y, t):

        xx=x-120+(t*120)%240

        pygame.draw.circle(
            surface,
            (180,180,255),
            (int(xx),y),
            5
        )

        pygame.draw.circle(
            surface,
            theme.WHITE,
            (int(xx),y),
            9,
            1
        )
    
    def draw_gluon(self, surface, x, y, t):

        pygame.draw.circle(surface,(255,0,255),(x-45,y),12)

        pygame.draw.circle(surface,(0,255,0),(x+45,y),12)

        for i in range(20):

            px=x-45+i*5

            py=y+math.sin(i+t*6)*6

            pygame.draw.circle(surface,(255,255,255),(int(px),int(py)),2)
      
    def draw_positron(self, surface, x, y, t):

        pygame.draw.circle(surface,(120,180,255),(x,y),12)

        pygame.draw.circle(surface,theme.WHITE,(x,y),60,2)

        angle=-t*2

        ex=x+math.cos(angle)*60
        ey=y+math.sin(angle)*60

        pygame.draw.circle(
            surface,
            (255,120,120),
            (int(ex),int(ey)),
            8
        )
        
    def draw_higgs(self, surface, x, y, t):

        pulse=1+0.15*math.sin(t*2)

        radius=int(35*pulse)

        pygame.draw.circle(
            surface,
            (255,180,0),
            (x,y),
            radius
        )

        for r in (60,90):

            rr=int(r+math.sin(t*2+r)*6)

            pygame.draw.circle(
                surface,
                (255,220,120),
                (x,y),
                rr,
                2
            )
        
    def draw_cards(self, surface, particle, rect):

        # DEBUG
        pygame.draw.rect(
            surface,
            (255, 180, 0),
            rect,
            2,
        )

    def draw_description(self, surface, particle, rect):

        # DEBUG
        pygame.draw.rect(
            surface,
            (0, 220, 120),
            rect,
            2,
        )